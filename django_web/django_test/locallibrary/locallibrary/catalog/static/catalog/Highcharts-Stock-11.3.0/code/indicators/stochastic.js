/**
 * Highstock JS v11.3.0 (2024-01-10)
 *
 * Indicator series type for Highcharts Stock
 *
 * (c) 2010-2024 Paweł Fus
 *
 * License: www.highcharts.com/license
 */!function(t){"object"==typeof module&&module.exports?(t.default=t,module.exports=t):"function"==typeof define&&define.amd?define("highcharts/indicators/stochastic",["highcharts","highcharts/modules/stock"],function(e){return t(e),t.Highcharts=e,t}):t("undefined"!=typeof Highcharts?Highcharts:void 0)}(function(t){"use strict";var e=t?t._modules:{};function i(t,e,i,o){t.hasOwnProperty(e)||(t[e]=o.apply(null,i),"function"==typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:e,module:t[e]}})))}i(e,"Stock/Indicators/ArrayUtilities.js",[],function(){return{getArrayExtremes:function(t,e,i){return t.reduce((t,o)=>[Math.min(t[0],o[e]),Math.max(t[1],o[i])],[Number.MAX_VALUE,-Number.MAX_VALUE])}}}),i(e,"Stock/Indicators/MultipleLinesComposition.js",[e["Core/Series/SeriesRegistry.js"],e["Core/Utilities.js"]],function(t,e){var i;let{sma:{prototype:o}}=t.seriesTypes,{defined:s,error:a,merge:r}=e;return function(t){let e=["bottomLine"],i=["top","bottom"],n=["top"];function l(t){return"plot"+t.charAt(0).toUpperCase()+t.slice(1)}function p(t,e){let i=[];return(t.pointArrayMap||[]).forEach(t=>{t!==e&&i.push(l(t))}),i}function h(){let t=this,e=t.pointValKey,i=t.linesApiNames,n=t.areaLinesNames,h=t.points,c=t.options,u=t.graph,d={options:{gapSize:c.gapSize}},f=[],m=p(t,e),y=h.length,g;if(m.forEach((t,e)=>{for(f[e]=[];y--;)g=h[y],f[e].push({x:g.x,plotX:g.plotX,plotY:g[t],isNull:!s(g[t])});y=h.length}),t.userOptions.fillColor&&n.length){let e=m.indexOf(l(n[0])),i=f[e],s=1===n.length?h:f[m.indexOf(l(n[1]))],a=t.color;t.points=s,t.nextPoints=i,t.color=t.userOptions.fillColor,t.options=r(h,d),t.graph=t.area,t.fillGraph=!0,o.drawGraph.call(t),t.area=t.graph,delete t.nextPoints,delete t.fillGraph,t.color=a}i.forEach((e,i)=>{f[i]?(t.points=f[i],c[e]?t.options=r(c[e].styles,d):a('Error: "There is no '+e+' in DOCS options declared. Check if linesApiNames are consistent with your DOCS line names."'),t.graph=t["graph"+e],o.drawGraph.call(t),t["graph"+e]=t.graph):a('Error: "'+e+" doesn't have equivalent in pointArrayMap. To many elements in linesApiNames relative to pointArrayMap.\"")}),t.points=h,t.options=c,t.graph=u,o.drawGraph.call(t)}function c(t){let e,i=[],s=[];if(t=t||this.points,this.fillGraph&&this.nextPoints){if((e=o.getGraphPath.call(this,this.nextPoints))&&e.length){e[0][0]="L",i=o.getGraphPath.call(this,t),s=e.slice(0,i.length);for(let t=s.length-1;t>=0;t--)i.push(s[t])}}else i=o.getGraphPath.apply(this,arguments);return i}function u(t){let e=[];return(this.pointArrayMap||[]).forEach(i=>{e.push(t[i])}),e}function d(){let t=this.pointArrayMap,e=[],i;e=p(this),o.translate.apply(this,arguments),this.points.forEach(o=>{t.forEach((t,s)=>{i=o[t],this.dataModify&&(i=this.dataModify.modifyValue(i)),null!==i&&(o[e[s]]=this.yAxis.toPixels(i,!0))})})}t.compose=function(t){let o=t.prototype;return o.linesApiNames=o.linesApiNames||e.slice(),o.pointArrayMap=o.pointArrayMap||i.slice(),o.pointValKey=o.pointValKey||"top",o.areaLinesNames=o.areaLinesNames||n.slice(),o.drawGraph=h,o.getGraphPath=c,o.toYData=u,o.translate=d,t}}(i||(i={})),i}),i(e,"Stock/Indicators/Stochastic/StochasticIndicator.js",[e["Stock/Indicators/ArrayUtilities.js"],e["Stock/Indicators/MultipleLinesComposition.js"],e["Core/Series/SeriesRegistry.js"],e["Core/Utilities.js"]],function(t,e,i,o){let{sma:s}=i.seriesTypes,{extend:a,isArray:r,merge:n}=o;class l extends s{init(){super.init.apply(this,arguments),this.options=n({smoothedLine:{styles:{lineColor:this.color}}},this.options)}getValues(e,i){let o=i.periods[0],s=i.periods[1],a=e.xData,n=e.yData,l=n?n.length:0,p=[],h=[],c=[],u,d,f,m=null,y,g;if(l<o||!r(n[0])||4!==n[0].length)return;let A=!0,x=0;for(g=o-1;g<l;g++){if(u=n.slice(g-o+1,g+1),d=(y=t.getArrayExtremes(u,2,1))[0],isNaN(f=(n[g][3]-d)/(y[1]-d)*100)&&A){x++;continue}A&&!isNaN(f)&&(A=!1);let e=h.push(a[g]);isNaN(f)?c.push([c[e-2]&&"number"==typeof c[e-2][0]?c[e-2][0]:null,null]):c.push([f,null]),g>=x+(o-1)+(s-1)&&(m=super.getValues({xData:h.slice(-s),yData:c.slice(-s)},{period:s}).yData[0]),p.push([a[g],f,m]),c[e-1][1]=m}return{values:p,xData:h,yData:c}}}return l.defaultOptions=n(s.defaultOptions,{params:{index:void 0,period:void 0,periods:[14,3]},marker:{enabled:!1},tooltip:{pointFormat:'<span style="color:{point.color}">●</span><b> {series.name}</b><br/>%K: {point.y}<br/>%D: {point.smoothed}<br/>'},smoothedLine:{styles:{lineWidth:1,lineColor:void 0}},dataGrouping:{approximation:"averages"}}),a(l.prototype,{areaLinesNames:[],nameComponents:["periods"],nameBase:"Stochastic",pointArrayMap:["y","smoothed"],parallelArrays:["x","y","smoothed"],pointValKey:"y",linesApiNames:["smoothedLine"]}),e.compose(l),i.registerSeriesType("stochastic",l),l}),i(e,"masters/indicators/stochastic.src.js",[],function(){})});