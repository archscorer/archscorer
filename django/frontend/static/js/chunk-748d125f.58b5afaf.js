(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-748d125f"],{a676:function(t,e,r){"use strict";r("caad"),r("13d5"),r("2532");var n=r("b85c");e["a"]={sum:function(t){return Array.isArray(t)&&t.length?t.reduce((function(t,e){return t+e})):null},participantOrder:function(t,e){if(t.class<e.class)return-1;if(t.class>e.class)return 1;if(t.sum>e.sum)return-1;if(t.sum<e.sum)return 1;if(t.shootoff&&e.shootoff){if(t.shootoff>e.shootoff)return-1;if(t.shootoff<e.shootoff)return 1}else{if(t.x>e.x)return-1;if(t.x<e.x)return 1}return 0},participantRank:function(t){var e,r={class:null,ord:1,sum:null,x:null},a=Object(n["a"])(t.sort(this.participantOrder));try{for(a.s();!(e=a.n()).done;){var s=e.value;s.class!==r.class&&(r.class=s.class,r.ord=1,r.place=1,r.sum=s.sum,r.x=s.x),(s.sum<r.sum||s.shootoff||s.x<r.x&&r.ord>3)&&(r.place=r.ord),s["place"]=r.place,r.x=s.x,r.sum=s.sum,r.ord+=1}}catch(u){a.e(u)}finally{a.f()}},getClass:function(t,e){return e&&e.includes(t.age_group+"_"+t.style)?t.age_group+"_"+t.style:t.age_group+t.archer.gender+t.style}}},fcd1:function(t,e,r){"use strict";r.r(e);var n=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("v-container",[r("v-layout",{attrs:{"text-center":"",wrap:""}},[r("v-card",[r("v-card-text",[r("p",[t._v("This part of the site has not been developed yet. Ideas what kind of statistics or graphs to collect or show would be most wolcome.")])])],1),null!==t.user.id?r("UserPastEvents"):t._e()],1)],1)},a=[],s=r("5530"),u=r("2f62"),o=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("v-card",{staticClass:"mt-5"},[r("v-card-text",[t._v(" List of your past events with scores will appear here "),r("v-data-table",{attrs:{dense:"","mobile-breakpoint":300,headers:t.p_table_header,items:t.p_table,"items-per-page":50,"multi-sort":""},scopedSlots:t._u([{key:"item.event",fn:function(e){return[t._v(" "+t._s(e.item.event)+" ("),r("router-link",{attrs:{to:{name:"event",params:{id:e.item.eId}}}},[t._v("link")]),t._v(") ")]}}])})],1)],1)},c=[],i=(r("7db0"),r("c740"),r("d81d"),r("a434"),r("b0c0"),r("b85c")),d=r("a676"),l={components:{},data:function(){return{}},computed:Object(s["a"])(Object(s["a"])({},Object(u["d"])({user:function(t){return t.user.user},participants:function(t){return t.events.participants},events:function(t){return t.events.events},courses:function(t){return t.courses.courses}})),{},{p_table_header:function(){return[{text:"Event",value:"event"},{text:"Date",value:"date",width:"120px"},{text:"Round",value:"round"},{text:"Course",value:"course"},{text:"Score",value:"score"}]},p_table:function(){var t=this,e=[];if(this.participants.length){var r,n=Object(i["a"])(this.participants);try{var a=function(){var n=r.value,a=t.events.find((function(t){return t.id===n.event}));if(a){var s,u=[],o=Object(i["a"])(n.scorecards);try{var c=function(){var r=s.value,n=a.rounds.find((function(t){return t.id===r.round})),o=t.courses.find((function(t){return t.id===n.course})),c=n.label,i=o.name,l=d["a"].sum(r.arrows.map((function(t){return t.score})));if("s"===o.type)return"continue";if("u"===o.type){var f=u.findIndex((function(t){return t.id===o.id}));if(-1===f)return u.push({id:o.id,score:l,round:c}),"continue";c=u[f].round+" + "+c,i="2 x "+i,l=u[f].score+l,u.splice(f,1)}e.push({eId:a.id,event:a.name,date:a.date_start,round:c,course:i,score:l})};for(o.s();!(s=o.n()).done;)c()}catch(l){o.e(l)}finally{o.f()}}};for(n.s();!(r=n.n()).done;)a()}catch(s){n.e(s)}finally{n.f()}}return e.sort((function(t,e){return t.date<e.date?-1:t.date>e.date?1:0}))}}),created:function(){var t,e=this,r=Object(i["a"])(this.user.archer.events);try{var n=function(){var r=t.value;e.participants.find((function(t){return t.id===r}))||e.$store.dispatch("events/getParticipant",r)};for(r.s();!(t=r.n()).done;)n()}catch(a){r.e(a)}finally{r.f()}this.$store.dispatch("events/getEvents")}},f=l,p=r("2877"),v=r("6544"),h=r.n(v),m=r("b0af"),b=r("99d9"),x=r("8fea"),_=Object(p["a"])(f,o,c,!1,null,null,null),y=_.exports;h()(_,{VCard:m["a"],VCardText:b["c"],VDataTable:x["a"]});var w={name:"Statistics",components:{UserPastEvents:y},data:function(){return{}},computed:Object(s["a"])({},Object(u["d"])({user:function(t){return t.user.user}}))},g=w,O=r("a523"),j=r("a722"),k=Object(p["a"])(g,n,a,!1,null,null,null);e["default"]=k.exports;h()(k,{VCard:m["a"],VCardText:b["c"],VContainer:O["a"],VLayout:j["a"]})}}]);
//# sourceMappingURL=chunk-748d125f.58b5afaf.js.map