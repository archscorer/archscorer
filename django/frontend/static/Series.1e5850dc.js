import{s as i,t as c,u,v as l,B as p,D as m,w as d,x as v,z as a,A as f,g as h,j as g}from"./index.27d05026.js";import{_ as $}from"./VChip.0fc94f43.js";var y=function(){var e=this,s=e.$createElement,t=e._self._c||s;return t(i,[e.series.length===0?t(c,[e._v("No series found in the database")]):e._e(),e._l(e.series,function(n){return t(u,{key:"series"+n.id,attrs:{to:{name:"series",params:{id:n.id}}}},[t(l,[t(p,[e._v(e._s(n.name)+" "+e._s(n.creator==e.user.email?"*":""))]),t(m,[n.date_start!=n.date_end?[e._v(" from "+e._s(n.date_start)+" to "+e._s(n.date_end)+" ")]:[e._v(" on "+e._s(n.date_start)+" ")]],2)],1),t(d,[n.type!=="open"?t($,{attrs:{small:"",color:e.chip_color(n.type)},domProps:{textContent:e._s(n.type)}}):e._e()],1)],1)})],2)},x=[];const S={computed:{...v({series:e=>e.series.series,user:e=>e.user.user})},methods:{chip_color(e){return e==="private"?"primary":e==="club"?"secondary":""}},created(){this.$store.dispatch("series/getSeries")}},r={};var C=a(S,y,x,!1,b,null,null,null);function b(e){for(let s in r)this[s]=r[s]}var o=function(){return C.exports}(),L=function(){var e=this,s=e.$createElement,t=e._self._c||s;return t(f,[t(h,[t(g,{staticClass:"pt-8 mt-5"},[t(o),t("small",[t("p",[e._v("series created by you are marked with '*'")])])],1)],1)],1)},V=[];const j={name:"Series",components:{SeriesList:o},data:()=>({})},_={};var I=a(j,L,V,!1,k,null,null,null);function k(e){for(let s in _)this[s]=_[s]}var E=function(){return I.exports}();export{E as default};