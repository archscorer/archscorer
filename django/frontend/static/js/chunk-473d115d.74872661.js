(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-473d115d"],{"74c6":function(s,t,e){"use strict";e.r(t);var a=function(){var s=this,t=s.$createElement,e=s._self._c||t;return s.s?e("v-container",[e("v-layout",{attrs:{wrap:""}},[e("v-card",[e("v-card-title",{domProps:{textContent:s._s(s.s.name)}}),e("v-card-text",[e("p",{domProps:{innerHTML:s._s(s.series_desciption)}})]),e("seriesSummary")],1)],1)],1):e("v-overlay",[e("v-progress-circular",{attrs:{indeterminate:"",size:"64"}})],1)},r=[],i=function(){var s=this,t=s.$createElement,e=s._self._c||t;return e("v-sheet",[e("v-card",{staticClass:"mb-5"},[e("v-card-title",[e("small",[s._v("Archers Summary")]),e("v-spacer"),e("v-text-field",{attrs:{"append-icon":"mdi-magnify",label:"Search","single-line":"","hide-details":""},model:{value:s.s_search,callback:function(t){s.s_search=t},expression:"s_search"}})],1),e("v-data-table",{attrs:{"mobile-breakpoint":300,dense:"",headers:s.s_table_header,items:s.s_table,search:s.s_search,loading:s.loading,"group-by":"class","multi-sort":"","items-per-page":50}})],1),s.s.club_ranking?e("v-card",[e("v-card-title",[e("small",[s._v("Clubs Summary")]),e("v-spacer")],1),e("v-data-table",{attrs:{"mobile-breakpoint":300,dense:"",headers:s.c_table_header,items:s.c_table,loading:s.loading,"multi-sort":"","items-per-page":15}})],1):s._e()],1)},n=[],l=e("a676"),o=e("2f62"),u={components:{},data:()=>({s_search:""}),computed:{...Object(o["d"])({user:s=>s.user.user}),s(){return this.$store.getters["series/seriesById"](parseInt(this.$route.params.id))},loading(){if(this.s_table.length)return!1;if(this.s)for(let s of this.s.stages)if(Array.isArray(s.participants))return!1;return!0},s_table_header(){if(this.s){let s=[{text:"Class",value:"class"},{text:"Place",value:"place",width:"1%"},{text:"Name",value:"name",width:"175px"},{text:"Club",value:"club"},{text:"Points",value:"points"},{text:"Sum",value:"sum"}];return s.push(...this.s.stages.map((function(s){return{text:s.name,value:"stage"+s.id.toString(),class:"stage-header"}})).reverse()),s}return[]},c_table_header(){if(this.s_table&&this.s.club_ranking){let s=[{text:"Place",value:"place",width:"1%"},{text:"Club",value:"club"},{text:"Points",value:"points"}];return s.push(...this.s.stages.map((function(s){return{text:s.name,value:"stage"+s.id.toString(),class:"stage-header"}})).reverse()),s}return[]},s_table(){if(this.s){let s=[];for(let t of this.s.stages){if(!Array.isArray(t.participants))continue;let e=t.rounds.find(s=>"s"===s.course_details.type);e=e?e.id:null;let a=t.participants.map(s=>({name:s.archer.full_name,class:l["a"].getClass(s,this.s.ignore_gender),id:s.archer.id+s.age_group+s.style,club:s.archer.club_details.name_short,sum:l["a"].sum(s.scorecards.filter(s=>s.round!==e).map(s=>s.score)),x:l["a"].sum(s.scorecards.filter(s=>s.round!==e).map(s=>s.spots)),shootoff:e?l["a"].sum(s.scorecards.filter(s=>s.round===e).map(s=>s.score)):null,progress:!0}));l["a"].participantRank(a);let r=a.reduce((s,t)=>s.set(t.class,(s.get(t.class)||0)+1),new Map),i={class:null,points:null};for(let n of a.filter(s=>s.sum>0)){n.class!==i.class&&(i.class=n.class,i.points=Math.min(this.s.points_max,r.get(n.class))),n.points=i.points>=n.place&&n.sum>0?i.points-n.place+1:0;let e=s.findIndex(s=>s.id===n.id);-1===e?(s.push({id:n.id,class:n.class,name:n.name,club:n.club,sum:[n.sum],points:[n.points]}),s[s.length-1]["stage"+t.id.toString()]=(n.points>0?n.points:"-")+" ("+n.sum+")"):(s[e].sum.push(n.sum),s[e].points.push(n.points),s[e]["stage"+t.id.toString()]=(n.points>0?n.points:"-")+" ("+n.sum+")")}}for(let t of s)t.sum.sort((function(s,e){return t.points[t.sum.indexOf(e)]-t.points[t.sum.indexOf(s)]})),t.points.sort((function(s,t){return t-s})),t.points.length>=this.s.participant_min&&(t.place=null),t.points.length>=this.s.participant_max?(t.points=l["a"].sum(t.points.slice(0,this.s.participant_max)),t.sum=l["a"].sum(t.sum.slice(0,this.s.participant_max))):(t.points=l["a"].sum(t.points),t.sum=l["a"].sum(t.sum));return s.sort((function(s,t){return s.class<t.class?-1:s.class>t.class||s.points<t.points?1:s.points>t.points?-1:s.sum<t.sum?1:s.sum>t.sum?-1:0})).map(s=>(s.class!==this.class&&(this.class=s.class,this.ord=1,this.place=1,this.points=s.points,this.sum=s.sum),null===s.place&&s.points>0&&((s.points<this.points||s.sum<this.sum)&&(this.place=this.ord),s.place=this.place,this.ord+=1,this.sum=s.sum,this.points=s.points),0===s.points&&(s.points="-"),s),{class:null,place:1,ord:1,sum:null,points:null}).sort((function(s,t){return s.class<t.class?-1:s.class>t.class||(s.place||9999)>(t.place||9999)?1:(s.place||9999)<(t.place||9999)?-1:0}))}return[]},c_table(){if(this.s_table.length&&this.s.club_ranking){let s=[];for(let t of this.s.stages){let e="stage"+t.id.toString(),a={};for(let s of this.s_table)if(s[e]){s.class in a||(a[s.class]={}),s.club in a[s.class]||(a[s.class][s.club]=[]);let t=parseInt(s[e].split(" ")[0])||0;a[s.class][s.club].push(t)}for(let t of Object.values(a))for(let a in t){let r=0;r=t[a].length>this.s.club_ranking_max?l["a"].sum(t[a].sort((function(s,t){return t-s})).splice(0,this.s.club_ranking_max)):l["a"].sum(t[a]);let i=s.findIndex(s=>s.club===a);-1===i?(s.push({club:a,place:null,points:r}),s[s.length-1][e]=r):(e in s[i]?s[i][e]+=r:s[i][e]=r,s[i].points+=r)}}return s.sort((function(s,t){return s.points>t.points?-1:s.points<t.points?1:0})).map(s=>(s.points<this.points&&(this.place=this.ord),s.place=this.place,this.points=s.points,this.ord+=1,s),{place:1,ord:1,points:null})}return[]}},methods:{}},c=u,p=e("2877"),d=e("6544"),m=e.n(d),h=e("b0af"),f=e("99d9"),g=e("8fea"),b=e("8dd9"),_=e("2fa4"),x=e("8654"),v=Object(p["a"])(c,i,n,!1,null,null,null),y=v.exports;m()(v,{VCard:h["a"],VCardTitle:f["d"],VDataTable:g["a"],VSheet:b["a"],VSpacer:_["a"],VTextField:x["a"]});var C={components:{seriesSummary:y},data:()=>({}),computed:{...Object(o["d"])({user:s=>s.user.user}),series_desciption(){return this.s.description.split("\n\n").join("</p><p>").split("\n").join("<br/>")},s(){return this.$store.getters["series/seriesById"](parseInt(this.$route.params.id))}},created(){this.$store.dispatch("series/updateSeries",parseInt(this.$route.params.id)).catch(()=>{this.$router.push("/series")})}},S=C,k=(e("8278"),e("a523")),V=e("a722"),w=e("a797"),O=e("490a"),$=Object(p["a"])(S,a,r,!1,null,null,null);t["default"]=$.exports;m()($,{VCard:h["a"],VCardText:f["c"],VCardTitle:f["d"],VContainer:k["a"],VLayout:V["a"],VOverlay:w["a"],VProgressCircular:O["a"]})},8278:function(s,t,e){"use strict";e("8b40")},"8b40":function(s,t,e){},a676:function(s,t,e){"use strict";t["a"]={sum(s){return Array.isArray(s)&&s.length?s.reduce((s,t)=>s+t):null},participantScore(s,t){return this.sum(s.scorecards.filter(s=>s.round!==t).map(s=>s.score))},participantOrder(s,t){if(s.class<t.class)return-1;if(s.class>t.class)return 1;if(null!==s.shootoff&&null!==t.shootoff){if(s.shootoff>t.shootoff)return-1;if(s.shootoff<t.shootoff)return 1}return s.progress>t.progress?-1:s.progress<t.progress?1:s.sum>t.sum?-1:s.sum<t.sum?1:s.x>t.x?-1:s.x<t.x?1:0},participantRank(s){let t={class:null,ord:1,sum:null,x:null};for(let e of s.sort(this.participantOrder))e.class!==t.class&&(t.class=e.class,t.ord=1,t.place=1,t.sum=e.sum,t.x=e.x),("undefined"!==typeof e.shootoff&&null!==e.shootoff||e.sum<t.sum||e.x<t.x&&t.place>3)&&(t.place=t.ord),e["place"]=e.progress?t.place:null,t.x=e.x,t.sum=e.sum,t.ord+=1},getClass(s,t){return t&&t.includes(s.age_group+"_"+s.style)?s.age_group+"_"+s.style:s.age_group+s.archer.gender+s.style},longestPrefix(s){let t=s[0];for(let e=1;e<=t.length;e++)if(!1===s.every(s=>s.substring(0,e)===t.substring(0,e)))return t.substring(0,e-1).trim();return t}}}}]);
//# sourceMappingURL=chunk-473d115d.74872661.js.map