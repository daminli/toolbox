from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.interfaces import SessionExtension
from sqlalchemy.orm import mapper, class_mapper, attributes, object_mapper
from sqlalchemy.orm.exc import UnmappedClassError, UnmappedColumnError
from sqlalchemy import Table, Column, ForeignKeyConstraint, Integer, String, DateTime
from sqlalchemy import event
from sqlalchemy.orm.properties import RelationshipProperty

def col_references_table(col, table):
    for fk in col.foreign_keys:
        if fk.references(table):
            return True
    return False


def _history_mapper(local_mapper):
    cls = local_mapper.class_

    # set the "active_history" flag
    # on on column-mapped attributes so that the old version
    # of the info is always loaded (currently sets it on all attributes)
    for prop in local_mapper.iterate_properties:
        getattr(local_mapper.class_, prop.key).impl.active_history = True

    super_mapper = local_mapper.inherits
    super_history_mapper = getattr(cls, '__history_mapper__', None)

    polymorphic_on = None
    super_fks = []

    if not super_mapper or local_mapper.local_table is not super_mapper.local_table:
        cols = []
        for column in local_mapper.local_table.c:
            if column.name in ['version','sys_created_by','sys_creation_date','sys_modified_by','sys_modified_date']:
                continue

            col = column.copy()
            col.unique = False

            if super_mapper and col_references_table(column, super_mapper.local_table):
                super_fks.append((col.key, list(super_history_mapper.local_table.primary_key)[0]))

            cols.append(col)

            if column is local_mapper.polymorphic_on:
                polymorphic_on = col

        if super_mapper:
            super_fks.append(('version', super_history_mapper.local_table.c.version))
            cols.append(Column('version', Integer, primary_key=True, autoincrement=False))
        else:
            cols.append(Column('version', Integer, primary_key=True, autoincrement=False))

        if super_fks:
            cols.append(ForeignKeyConstraint(*zip(*super_fks)))
            
        cols.append(Column('action', String(10)))
        cols.append(Column('action_by', String(32), default=get_userid, doc='user id'))
        cols.append(Column('sys_timestamp', DateTime, primary_key=True, default=datetime.now, doc='the action time'))
                
        table = Table(local_mapper.local_table.name + '_his', local_mapper.local_table.metadata,
           *cols
        )
    else:
        # single table inheritance.  take any additional columns that may have
        # been added and add them to the history table.
        for column in local_mapper.local_table.c:
            if column.key not in super_history_mapper.local_table.c:
                col = column.copy()
                col.unique = False
                super_history_mapper.local_table.append_column(col)
        table = None

    if super_history_mapper:
        bases = (super_history_mapper.class_,)
    else:
        bases = local_mapper.base_mapper.class_.__bases__
    versioned_cls = type.__new__(type, "%sHistory" % cls.__name__, bases, {})

    m = mapper(
            versioned_cls,
            table,
            inherits=super_history_mapper,
            polymorphic_on=polymorphic_on,
            polymorphic_identity=local_mapper.polymorphic_identity
            )
    cls.__history_mapper__ = m

    if not super_history_mapper:
        local_mapper.local_table.append_column(
            Column('version', Integer, default=1, nullable=False)
        )
        local_mapper.add_property("version", local_mapper.local_table.c.version)


class SmartTable(object):
    '''
    class attribute:
    __audit_trail__ = False
    '''
    __sys_attr__ = True
    __audit_trail__ = False
   
    @declared_attr
    def __mapper_cls__(cls):
        def map(cls, *arg, **kw):
            mp = mapper(cls, *arg, **kw)
            if cls.__sys_attr__:
                _sys_attr(mp)
            if cls.__audit_trail__:
                _history_mapper(mp)
            return mp
        return map
    
def versioned_objects(iter):
    for obj in iter:
        if hasattr(obj, '__history_mapper__'):
            yield obj

def create_version(obj, session, action):
    print action
    obj_mapper = object_mapper(obj)
    history_mapper = obj.__history_mapper__
    history_cls = history_mapper.class_

    obj_state = attributes.instance_state(obj)

    attr = {}

    obj_changed = False

    for om, hm in zip(obj_mapper.iterate_to_root(), history_mapper.iterate_to_root()):
        if hm.single:
            continue

        for hist_col in hm.local_table.c:
            if hist_col.key in ['version', 'action', 'sys_timestamp','action_by']:
                continue

            obj_col = om.local_table.c[hist_col.key]

            # get the value of the
            # attribute based on the MapperProperty related to the
            # mapped column.  this will allow usage of MapperProperties
            # that have a different keyname than that of the mapped column.
            try:
                prop = obj_mapper.get_property_by_column(obj_col)
            except UnmappedColumnError:
                # in the case of single table inheritance, there may be
                # columns on the mapped table intended for the subclass only.
                # the "unmapped" status of the subclass column on the
                # base class is a feature of the declarative module as of sqla 0.5.2.
                continue

            # expired object attributes and also deferred cols might not be in the
            # dict.  force it to load no matter what by using getattr().
            if prop.key not in obj_state.dict:
                getattr(obj, prop.key)
            attr[hist_col.key] = getattr(obj, prop.key)

            a, u, d = attributes.get_history(obj, prop.key)

            if d:
                # attr[hist_col.key] = d[0]
                obj_changed = True
            elif u:
                attr[hist_col.key] = u[0]
            else:
                # if the attribute had no value.
                # attr[hist_col.key] = a[0]
                obj_changed = True

    if not obj_changed:
        # not changed, but we have relationships.  OK
        # check those too
        for prop in obj_mapper.iterate_properties:
            if isinstance(prop, RelationshipProperty) and \
                attributes.get_history(obj, prop.key).has_changes():
                for p in prop.local_columns:
                    if p.foreign_keys:
                        obj_changed = True
                        break
                if obj_changed is True:
                    break

    if not obj_changed and action != 'DELETE':
        return
    
    if obj.version:
        obj.version += 1
    else:
        obj.version = 1
    attr['version'] = obj.version
    attr['action'] = action
    attr['action_by'] = get_userid()
    attr['sys_timestamp'] = datetime.now()
    hist = history_cls()
    for key, value in attr.items():
        setattr(hist, key, value)
    session.add(hist)

class SmartTableExtension(SessionExtension):
    def before_flush(self, session, flush_context, instances):
        for obj in versioned_objects(session.new):
            create_version(obj, session, 'INSERT')
        for obj in versioned_objects(session.dirty):
            create_version(obj, session, 'UPDATE')
        for obj in versioned_objects(session.deleted):
            create_version(obj, session, 'DELETE')
            

def _sys_attr(local_mapper):
    '''
    system attribute:
        ent_status : [ACTIVE,DELETED] usered to logic deleted
        modified_date : last modified date for this record
        modified_by: last modified user id
        creation_date : creation data  for this record
        created_by : who create this record    
    '''

    cls = local_mapper.class_
    super_sys = getattr(cls, '__do_sys_attr__', None)
    if not super_sys:
        cls.__do_sys_attr__ = True
        local_mapper.local_table.append_column(Column('sys_ent_status', String(10), default='ACTIVE'))
        local_mapper.local_table.append_column(Column('sys_creation_date', DateTime))
        local_mapper.local_table.append_column(Column('sys_created_by', String(32)))
        local_mapper.local_table.append_column(Column('sys_modified_date', DateTime))
        local_mapper.local_table.append_column(Column('sys_modified_by', String(32)))
        local_mapper.add_property("ent_status", local_mapper.local_table.c.sys_ent_status)
        local_mapper.add_property("creation_date", local_mapper.local_table.c.sys_creation_date)
        local_mapper.add_property("created_by", local_mapper.local_table.c.sys_created_by)
        local_mapper.add_property("modified_date", local_mapper.local_table.c.sys_modified_date)
        local_mapper.add_property("modified_by", local_mapper.local_table.c.sys_modified_by)
        
        event.listen(cls, 'before_insert', before_insert)
        event.listen(cls, 'before_update', before_update)

def before_insert(mapper, connection, target):
    target.created_by=get_userid()
    target.creation_date=datetime.now()
    target.modified_by=get_userid()
    target.modified_date=datetime.now()
 
def before_update(mapper, connection, target):
    target.modified_by=get_userid()
    target.modified_date=datetime.now()

def get_userid():
    return 'lidm1'