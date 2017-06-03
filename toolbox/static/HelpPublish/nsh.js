// NS-Header and page initialization

function pageOffset(win)
{
    if(!win) win = window;
    var pos = {left:0,top:0};

    if(typeof win.pageXOffset != 'undefined')
    {
         // Mozilla/Netscape
         pos.left = win.pageXOffset;
         pos.top = win.pageYOffset;
    }
    else
    {
         var obj = (win.document.compatMode && win.document.compatMode == "CSS1Compat") ?
         win.document.documentElement : win.document.body || null;

         pos.left = obj.scrollLeft;
         pos.top = obj.scrollTop;
    }
    return pos;
}

   function doResize() { 
     var clheight, headheight;
     if (self.innerHeight) // all except Explorer 
     { clheight = self.innerHeight; } 
     else if (document.documentElement && document.documentElement.clientHeight) // Explorer 6 Strict Mode 
     { clheight = document.documentElement.clientHeight; } 
     else if (document.body) // other Explorers 
     { clheight = document.body.clientHeight; } 
     headheight = document.getElementById('idheader').clientHeight;
     if (clheight < headheight ) {clheight = headheight + 1;}
     document.getElementById('idcontent').style.height = clheight - document.getElementById('idheader').clientHeight +'px'; 
   } 

   function nsrInit() { 
     contentbody = document.getElementById('idcontent'); 
     if (contentbody) { 
       aTop = pageOffset.top; //document.getElementById('body').scrollTop; 
       contentbody.className = 'nonscroll'; 
       document.getElementsByTagName('body')[0].className = 'nonscroll'; 
       document.getElementsByTagName('html')[0].className = 'nonscroll'; 
       window.onresize = doResize; 
       doResize(); 
       if (contentbody.scrollTo) { contentbody.scrollTo(aTop,0); }
      } 
   } 
 
// Toggle Toggler 

var toggleCount=false;
var switchState;

function toggleToggles() {

    if (!toggleCount) {
     toggleCount = true;
     HMToggleExpandAll(true);
     switchState = true;
     }
   
     else if (switchState) {
        HMToggleExpandAll(false);
        switchState = false;
        }
        
     else  {
        HMToggleExpandAll(true);
        switchState = true;
        } 
    }
   
// Page Init

function doInit() {
var lastSlashPos = document.URL.lastIndexOf("/") >
document.URL.lastIndexOf("\\") ? document.URL.lastIndexOf("/") :
document.URL.lastIndexOf("\\");
if( document.URL.substring( lastSlashPos + 1, lastSlashPos + 4
).toLowerCase() != "~hh" )
    {
    nsrInit();
    }
}


// Dynamic Topic TOC

function getElementsByClass(node,searchClass,tag) {
var classElements = new Array();
var els = node.getElementsByTagName(tag); 
var elsLen = els.length;
var pattern = new RegExp("\\bf_(.+)?"+searchClass+"(.+)?\\b");
for (i = 0, j = 0; i < elsLen; i++) {
 if ( pattern.test(els[i].className) ) {
 classElements[j] = els[i];
 j++;
 }
}
return classElements;t
}

 
function dynTOCinit() {
var dyntoc = document.getElementById("autotoc"); 
var el = getElementsByClass(document,'AutoTOC','span');
var tocmenu = '';
var newAnchor ='';
var tocentry = '';
var tocPos = GetTOCvars('float');
var tocTitle = GetTOCvars('title');
var tocHeadBG = GetTOCvars('headbg');
var tocLimit = GetTOCvars('limit')-1;
var autoTOC = GetTOCvars('autotoc');


if (document.all) {
  var sFloat="styleFloat"; // MSIE
} else {
  var sFloat="cssFloat"; // Real browsers
}

if ((el.length > tocLimit) && (GetTOCvars('autotoc'))) {
 for (i=0; i<el.length; i++) {
   tocentry = el[i];
   newAnchor = 'headline_' + i;
   tocentry.setAttribute('id',newAnchor,0);
   tocmenu = tocmenu +  '<p class="p_DynTOCItems"><span class="f_DynTOCItems"><a href="#' + newAnchor + '">' + tocentry.innerHTML + '</a></span></p>'; 
}

finaltocmenu = '<table border="2" cellpadding="4" id="dyntoctable"><tr><td align="center" bgcolor="' + tocHeadBG + '"><p class="p_DynTOCHeader"><span class="f_DynTOCHeader">' + tocTitle + '</span></p></td></tr><tr><td style="white-space:nowrap;">' + tocmenu + '</td></tr></table>';
if (tocPos == 'left') {dyntoc.style.margin = '0 8px 0 0';
					   dyntoc.style[sFloat] = 'left';}
else if (tocPos == 'right') {dyntoc.style.margin = '0 0 0 4px';
							dyntoc.style[sFloat] = 'right';}
else {dyntoc.style.margin = '10px auto 20px auto';
					  dyntoc.style[sFloat] = 'none';
                      dyntoc.style.width = '100%';
                      finaltocmenu= '<table width="100%" cellpadding=0" cellspacing="0" border="0"><tr><td align="center" width="100%">' + finaltocmenu + '</td></tr></table>'; } 
dyntoc.innerHTML = finaltocmenu;

}}
