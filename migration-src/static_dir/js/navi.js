// Menu-JavaScript [2009.03.31-combo]

function reloadPage(init) {  //reloads the window if Nav4 resized
if (init==true) with (navigator) {if ((appName=="Netscape")&&(parseInt(appVersion)==4)) {
document.pgW=innerWidth; document.pgH=innerHeight; onresize=reloadPage; }}
else if (innerWidth!=document.pgW || innerHeight!=document.pgH) location.reload();
}
reloadPage(true);

function findObj(n, d) { //v4.01
var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=findObj(n,d.layers[i].document);
if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function showHideLayers() { //v6.0
var i,p,v,obj,args=showHideLayers.arguments;
for (i=0; i<(args.length-2); i+=3) if ((obj=findObj(args[i]))!=null) { v=args[i+2];
if (obj.style) { obj=obj.style; v=(v=='show')?'visible':(v=='hide')?'hidden':v; }
obj.visibility=v; }
}

function preloadImages() { //v3.0
var d=document; if(d.images){ if(!d.p) d.p=new Array();
var i,j=d.p.length,a=preloadImages.arguments; for(i=0; i<a.length; i++)
if (a[i].indexOf("#")!=0){ d.p[j]=new Image; d.p[j++].src=a[i];}}
}

function swapImgRestore() { //v3.0
var i,x,a=document.sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function swapImage() { //v3.0
var i,j=0,x,a=swapImage.arguments; document.sr=new Array; for(i=0;i<(a.length-2);i+=3)
if ((x=findObj(a[i]))!=null){document.sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}

if(navigator.userAgent.indexOf("Firefox") >= 0){
document.write("<link rel='stylesheet' type='text/css' href='css/firefox.css'>");
}else if(navigator.userAgent.indexOf("Safari") >= 0){
document.write("<link rel='stylesheet' type='text/css' href='css/safari.css'>");
}else{
document.write("<link rel='stylesheet' type='text/css' href='css/ie.css'>");
}

var TimeOut         = 200;
var currentLayer    = null;
var currentitem     = null;
var currentLayerNum = 0;
var noClose         = 0;
var closeTimer      = null;

function mopen(n) {
  var l  = document.getElementById("menu" + n);
  var mm = document.getElementById("mmenu" + n);
	
  if(l) {
    mcancelclosetime();
    l.style.visibility='visible';
    if(currentLayer && (currentLayerNum != n))
      currentLayer.style.visibility='hidden';
    currentLayer = l;
    currentitem = mm;
    currentLayerNum = n;			
  } else if(currentLayer) {
    currentLayer.style.visibility='hidden';
    currentLayerNum = 0;
    currentitem = null;
    currentLayer = null;
 	}
}

function mclosetime() {
  closeTimer = window.setTimeout(mclose, TimeOut);
}

function mcancelclosetime() {
  if(closeTimer) {
    window.clearTimeout(closeTimer);
    closeTimer = null;
  }
}

function mclose() {
  if(currentLayer && noClose!=1)   {
    currentLayer.style.visibility='hidden';
    currentLayerNum = 0;
    currentLayer = null;
    currentitem = null;
  } else {
    noClose = 0;
  }
  currentLayer = null;
  currentitem = null;
}

document.onclick = mclose; 