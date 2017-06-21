# coding=utf-8
'''
Created on 2013-4-27

@author= lidm1
'''
"""
id: the unique id for the navigation node
text: the display name for a function or folder
icon: menu icon
activity: function Authorization Principal name
target: the function target, normally it is a valid url 
type: the function type, now it is url

the navigation view is composed of  a list of tree panel, which title and icon is define in the data firrt level
children: the tree navigation data
children: tree children
expanded: the tree node is expended or not
"""

'''
import user_security
import free_query
import sql_executor
import common
import workflow_report
import itsm
import action
'''

favorit = dict(
            id="temp",
            text='Favorit',
            iconCls='x-fa fa-home',
            expanded=True,
            children=[dict(
                        id='upload',
                        text='Excel Upload',
                        target='/extpage/common/Upload/',
                        type='url'
                    ),dict(
                        id='baidu',
                        text='Baidu Searching',
                        activity='ScheduleCalendar',
                        target='http://www.baidu.com',
                        type='url'
                    ), dict(
                        id='IconsGlyph',
                        text='Icons Glyph',
                        activity='IconsGlyph',
                        target='/extpage/tools/IconsGlyph/',
                        type='url'
                    ), dict(
                        id='UserAuth',
                        text='User Auth',
                        activity='User Auth',
                        target='/extpage/main/UserAuth/',
                        type='url'
                        
                    ), dict(
                        id='Dg',
                        text='Dg Page',
                        activity='Dg',
                        target='/extpage/common/Dg/',
                        type='url'
                    )]
        )

NAV_DATA=[favorit]
