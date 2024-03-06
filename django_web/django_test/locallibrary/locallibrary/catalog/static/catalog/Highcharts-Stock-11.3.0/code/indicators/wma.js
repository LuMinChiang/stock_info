/**
 * Highstock JS v11.3.0 (2024-01-10)
 *
 * Indicator series type for Highcharts Stock
 *
 * (c) 2010-2024 Kacper Madej
 *
 * License: www.highcharts.com/license
 */!function(e){"object"==typeof module&&module.exports?(e.default=e,module.exports=e):"function"==typeof define&&define.amd?define("highcharts/indicators/wma",["highcharts","highcharts/modules/stock"],function(t){return e(t),e.Highcharts=t,e}):e("undefined"!=typeof Highcharts?Highcharts:void 0)}(function(e){"use strict";var t=e?e._modules:{};function s(e,t,s,n){e.hasOwnProperty(t)||(e[t]=n.apply(null,s),"function"==typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:t,module:e[t]}})))}s(t,"Stock/Indicators/WMA/WMAIndicator.js",[t["Core/Series/SeriesRegistry.js"],t["Core/Utilities.js"]],function(e,t){let{sma:s}=e.seriesTypes,{isArray:n,merge:i}=t;function r(e,t,s,n,i){let r=t[n],o=i<0?s[n]:s[n][i];e.push([r,o])}function o(e,t,s,n){let i=e.length,r=e.reduce(function(e,t,s){return[null,e[1]+t[1]*(s+1)]})[1]/((i+1)/2*i),o=t[n-1];return e.shift(),[o,r]}class u extends s{getValues(e,t){let s=t.period,i=e.xData,u=e.yData,a=u?u.length:0,d=i[0],h=[],c=[],l=[],f=1,p=-1,m,g,y=u[0];if(i.length<s)return;n(u[0])&&(p=t.index,y=u[0][p]);let w=[[d,y]];for(;f!==s;)r(w,i,u,f,p),f++;for(m=f;m<a;m++)h.push(g=o(w,i,u,m)),c.push(g[0]),l.push(g[1]),r(w,i,u,m,p);return h.push(g=o(w,i,u,m)),c.push(g[0]),l.push(g[1]),{values:h,xData:c,yData:l}}}return u.defaultOptions=i(s.defaultOptions,{params:{index:3,period:9}}),e.registerSeriesType("wma",u),u}),s(t,"masters/indicators/wma.src.js",[],function(){})});