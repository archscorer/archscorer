(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2bc8ebd0"],{"08ea":function(e,t,s){},"0fd9":function(e,t,s){"use strict";s("4b85");var a=s("2b0e"),n=s("d9f7"),r=s("80d2");const i=["sm","md","lg","xl"],l=["start","end","center"];function c(e,t){return i.reduce((s,a)=>(s[e+Object(r["G"])(a)]=t(),s),{})}const o=e=>[...l,"baseline","stretch"].includes(e),u=c("align",()=>({type:String,default:null,validator:o})),d=e=>[...l,"space-between","space-around"].includes(e),h=c("justify",()=>({type:String,default:null,validator:d})),p=e=>[...l,"space-between","space-around","stretch"].includes(e),f=c("alignContent",()=>({type:String,default:null,validator:p})),m={align:Object.keys(u),justify:Object.keys(h),alignContent:Object.keys(f)},g={align:"align",justify:"justify",alignContent:"align-content"};function v(e,t,s){let a=g[e];if(null!=s){if(t){const s=t.replace(e,"");a+="-"+s}return a+="-"+s,a.toLowerCase()}}const b=new Map;t["a"]=a["a"].extend({name:"v-row",functional:!0,props:{tag:{type:String,default:"div"},dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:o},...u,justify:{type:String,default:null,validator:d},...h,alignContent:{type:String,default:null,validator:p},...f},render(e,{props:t,data:s,children:a}){let r="";for(const n in t)r+=String(t[n]);let i=b.get(r);if(!i){let e;for(e in i=[],m)m[e].forEach(s=>{const a=t[s],n=v(e,s,a);n&&i.push(n)});i.push({"no-gutters":t.noGutters,"row--dense":t.dense,["align-"+t.align]:t.align,["justify-"+t.justify]:t.justify,["align-content-"+t.alignContent]:t.alignContent}),b.set(r,i)}return e(t.tag,Object(n["a"])(s,{staticClass:"row",class:i}),a)}})},2151:function(e,t,s){"use strict";var a=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("v-autocomplete",{attrs:{"search-input":e.query,items:e.qresponse_items,label:"Find archer ...",hint:"Search is executed from 2 characters",placeholder:"Start typing ..","prepend-icon":"mdi-database-search","return-object":"","hide-no-data":"","no-filter":"",clearable:""},on:{input:function(t){return e.$emit("input",e.archer)},"update:searchInput":function(t){e.query=t},"update:search-input":function(t){e.query=t}},model:{value:e.archer,callback:function(t){e.archer=t},expression:"archer"}})},n=[],r=s("2f62"),i={props:{value:Object},data:()=>({archer:{},query:""}),watch:{query:function(e){e&&e.length>=2?this.searchArcher(e):this.clearSearch([{header:"be more specific (at least 2 letters)"}])}},computed:{...Object(r["d"])({qresponse:e=>e.user.qresponse,clubs:e=>e.clubs.clubs}),qresponse_items(){return this.qresponse.map(e=>{if(e.id){let t=e.full_name+" ("+this.clubs.find(t=>t.id===e.club).name_short+")"+(e.user?" - w account":"")+(e.events.length?" "+e.events.length+" events":"");return Object.assign({},e,{text:t})}return e})}},methods:{...Object(r["b"])("user",["searchArcher","clearSearch"])},created(){this.$store.dispatch("clubs/getClubs")}},l=i,c=s("2877"),o=s("6544"),u=s.n(o),d=s("c6a6"),h=Object(c["a"])(l,a,n,!1,null,null,null);t["a"]=h.exports;u()(h,{VAutocomplete:d["a"]})},"2bfd":function(e,t,s){},"62ad":function(e,t,s){"use strict";s("4b85");var a=s("2b0e"),n=s("d9f7"),r=s("80d2");const i=["sm","md","lg","xl"],l=(()=>i.reduce((e,t)=>(e[t]={type:[Boolean,String,Number],default:!1},e),{}))(),c=(()=>i.reduce((e,t)=>(e["offset"+Object(r["G"])(t)]={type:[String,Number],default:null},e),{}))(),o=(()=>i.reduce((e,t)=>(e["order"+Object(r["G"])(t)]={type:[String,Number],default:null},e),{}))(),u={col:Object.keys(l),offset:Object.keys(c),order:Object.keys(o)};function d(e,t,s){let a=e;if(null!=s&&!1!==s){if(t){const s=t.replace(e,"");a+="-"+s}return"col"!==e||""!==s&&!0!==s?(a+="-"+s,a.toLowerCase()):a.toLowerCase()}}const h=new Map;t["a"]=a["a"].extend({name:"v-col",functional:!0,props:{cols:{type:[Boolean,String,Number],default:!1},...l,offset:{type:[String,Number],default:null},...c,order:{type:[String,Number],default:null},...o,alignSelf:{type:String,default:null,validator:e=>["auto","start","end","center","baseline","stretch"].includes(e)},tag:{type:String,default:"div"}},render(e,{props:t,data:s,children:a,parent:r}){let i="";for(const n in t)i+=String(t[n]);let l=h.get(i);if(!l){let e;for(e in l=[],u)u[e].forEach(s=>{const a=t[s],n=d(e,s,a);n&&l.push(n)});const s=l.some(e=>e.startsWith("col-"));l.push({col:!s||!t.cols,["col-"+t.cols]:t.cols,["offset-"+t.offset]:t.offset,["order-"+t.order]:t.order,["align-self-"+t.alignSelf]:t.alignSelf}),h.set(i,l)}return e(t.tag,Object(n["a"])(s,{class:l}),a)}})},a676:function(e,t,s){"use strict";t["a"]={sum(e){return Array.isArray(e)&&e.length?e.reduce((e,t)=>e+t):null},participantScore(e,t){return this.sum(e.scorecards.filter(e=>e.round!==t).map(e=>e.score))},participantOrder(e,t){if(e.class<t.class)return-1;if(e.class>t.class)return 1;if(null!==e.shootoff&&null!==t.shootoff){if(e.shootoff>t.shootoff)return-1;if(e.shootoff<t.shootoff)return 1}return e.sum>t.sum?-1:e.sum<t.sum?1:e.x>t.x?-1:e.x<t.x?1:0},participantRank(e){let t={class:null,ord:1,sum:null,x:null};for(let s of e.sort(this.participantOrder))s.class!==t.class&&(t.class=s.class,t.ord=1,t.place=1,t.sum=s.sum,t.x=s.x),("undefined"!==typeof s.shootoff&&null!==s.shootoff||s.sum<t.sum||s.x<t.x&&t.place>3)&&(t.place=t.ord),s["place"]=t.place,t.x=s.x,t.sum=s.sum,t.ord+=1},getClass(e,t){return t&&t.includes(e.age_group+"_"+e.style)?e.age_group+"_"+e.style:e.age_group+e.archer.gender+e.style},longestPrefix(e){let t=e[0];for(let s=1;s<t.length;s++)if(!1===e.every(e=>e.substring(0,s)===t.substring(0,s)))return t.substring(0,s-1);return t}}},c6a6:function(e,t,s){"use strict";s("2bfd");var a=s("b974"),n=s("8654"),r=s("d9f7"),i=s("80d2");const l={...a["b"],offsetY:!0,offsetOverflow:!0,transition:!1};t["a"]=a["a"].extend({name:"v-autocomplete",props:{allowOverflow:{type:Boolean,default:!0},autoSelectFirst:{type:Boolean,default:!1},filter:{type:Function,default:(e,t,s)=>s.toLocaleLowerCase().indexOf(t.toLocaleLowerCase())>-1},hideNoData:Boolean,menuProps:{type:a["a"].options.props.menuProps.type,default:()=>l},noFilter:Boolean,searchInput:{type:String}},data(){return{lazySearch:this.searchInput}},computed:{classes(){return{...a["a"].options.computed.classes.call(this),"v-autocomplete":!0,"v-autocomplete--is-selecting-index":this.selectedIndex>-1}},computedItems(){return this.filteredItems},selectedValues(){return this.selectedItems.map(e=>this.getValue(e))},hasDisplayedItems(){return this.hideSelected?this.filteredItems.some(e=>!this.hasItem(e)):this.filteredItems.length>0},currentRange(){return null==this.selectedItem?0:String(this.getText(this.selectedItem)).length},filteredItems(){return!this.isSearching||this.noFilter||null==this.internalSearch?this.allItems:this.allItems.filter(e=>{const t=Object(i["s"])(e,this.itemText),s=null!=t?String(t):"";return this.filter(e,String(this.internalSearch),s)})},internalSearch:{get(){return this.lazySearch},set(e){this.lazySearch!==e&&(this.lazySearch=e,this.$emit("update:search-input",e))}},isAnyValueAllowed(){return!1},isDirty(){return this.searchIsDirty||this.selectedItems.length>0},isSearching(){return this.multiple&&this.searchIsDirty||this.searchIsDirty&&this.internalSearch!==this.getText(this.selectedItem)},menuCanShow(){return!!this.isFocused&&(this.hasDisplayedItems||!this.hideNoData)},$_menuProps(){const e=a["a"].options.computed.$_menuProps.call(this);return e.contentClass=("v-autocomplete__content "+(e.contentClass||"")).trim(),{...l,...e}},searchIsDirty(){return null!=this.internalSearch&&""!==this.internalSearch},selectedItem(){return this.multiple?null:this.selectedItems.find(e=>this.valueComparator(this.getValue(e),this.getValue(this.internalValue)))},listData(){const e=a["a"].options.computed.listData.call(this);return e.props={...e.props,items:this.virtualizedItems,noFilter:this.noFilter||!this.isSearching||!this.filteredItems.length,searchInput:this.internalSearch},e}},watch:{filteredItems:"onFilteredItemsChanged",internalValue:"setSearch",isFocused(e){e?(document.addEventListener("copy",this.onCopy),this.$refs.input&&this.$refs.input.select()):(document.removeEventListener("copy",this.onCopy),this.$refs.input&&this.$refs.input.blur(),this.updateSelf())},isMenuActive(e){!e&&this.hasSlot&&(this.lazySearch=null)},items(e,t){t&&t.length||!this.hideNoData||!this.isFocused||this.isMenuActive||!e.length||this.activateMenu()},searchInput(e){this.lazySearch=e},internalSearch:"onInternalSearchChanged",itemText:"updateSelf"},created(){this.setSearch()},destroyed(){document.removeEventListener("copy",this.onCopy)},methods:{onFilteredItemsChanged(e,t){e!==t&&(this.setMenuIndex(-1),this.$nextTick(()=>{this.internalSearch&&(1===e.length||this.autoSelectFirst)&&(this.$refs.menu.getTiles(),this.setMenuIndex(0))}))},onInternalSearchChanged(){this.updateMenuDimensions()},updateMenuDimensions(){this.isMenuActive&&this.$refs.menu&&this.$refs.menu.updateDimensions()},changeSelectedIndex(e){this.searchIsDirty||(this.multiple&&e===i["y"].left?-1===this.selectedIndex?this.selectedIndex=this.selectedItems.length-1:this.selectedIndex--:this.multiple&&e===i["y"].right?this.selectedIndex>=this.selectedItems.length-1?this.selectedIndex=-1:this.selectedIndex++:e!==i["y"].backspace&&e!==i["y"].delete||this.deleteCurrentItem())},deleteCurrentItem(){const e=this.selectedIndex,t=this.selectedItems[e];if(!this.isInteractive||this.getDisabled(t))return;const s=this.selectedItems.length-1;if(-1===this.selectedIndex&&0!==s)return void(this.selectedIndex=s);const a=this.selectedItems.length,n=e!==a-1?e:e-1,r=this.selectedItems[n];r?this.selectItem(t):this.setValue(this.multiple?[]:null),this.selectedIndex=n},clearableCallback(){this.internalSearch=null,a["a"].options.methods.clearableCallback.call(this)},genInput(){const e=n["a"].options.methods.genInput.call(this);return e.data=Object(r["a"])(e.data,{attrs:{"aria-activedescendant":Object(i["q"])(this.$refs.menu,"activeTile.id"),autocomplete:Object(i["q"])(e.data,"attrs.autocomplete","off")},domProps:{value:this.internalSearch}}),e},genInputSlot(){const e=a["a"].options.methods.genInputSlot.call(this);return e.data.attrs.role="combobox",e},genSelections(){return this.hasSlot||this.multiple?a["a"].options.methods.genSelections.call(this):[]},onClick(e){this.isInteractive&&(this.selectedIndex>-1?this.selectedIndex=-1:this.onFocus(),this.isAppendInner(e.target)||this.activateMenu())},onInput(e){if(this.selectedIndex>-1||!e.target)return;const t=e.target,s=t.value;t.value&&this.activateMenu(),this.internalSearch=s,this.badInput=t.validity&&t.validity.badInput},onKeyDown(e){const t=e.keyCode;!e.ctrlKey&&[i["y"].home,i["y"].end].includes(t)||a["a"].options.methods.onKeyDown.call(this,e),this.changeSelectedIndex(t)},onSpaceDown(e){},onTabDown(e){a["a"].options.methods.onTabDown.call(this,e),this.updateSelf()},onUpDown(e){e.preventDefault(),this.activateMenu()},selectItem(e){a["a"].options.methods.selectItem.call(this,e),this.setSearch()},setSelectedItems(){a["a"].options.methods.setSelectedItems.call(this),this.isFocused||this.setSearch()},setSearch(){this.$nextTick(()=>{this.multiple&&this.internalSearch&&this.isMenuActive||(this.internalSearch=!this.selectedItems.length||this.multiple||this.hasSlot?null:this.getText(this.selectedItem))})},updateSelf(){(this.searchIsDirty||this.internalValue)&&(this.valueComparator(this.internalSearch,this.getValue(this.internalValue))||this.setSearch())},hasItem(e){return this.selectedValues.indexOf(this.getValue(e))>-1},onCopy(e){var t,s;if(-1===this.selectedIndex)return;const a=this.selectedItems[this.selectedIndex],n=this.getText(a);null==(t=e.clipboardData)||t.setData("text/plain",n),null==(s=e.clipboardData)||s.setData("text/vnd.vuetify.autocomplete.item+plain",n),e.preventDefault()}}})},d0d5:function(e,t,s){"use strict";s("08ea")},fcd1:function(e,t,s){"use strict";s.r(t);var a=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("v-container",[s("v-layout",{staticClass:"d-flex justify-space-around",attrs:{wrap:""}},[s("v-card",[s("v-card-text",[s("p",[e._v("Work in progress. Ideas what kind of statistics or graphs to collect or show would be most wolcome.")])])],1),null!==e.user.id?s("ArcherPastEvents"):e._e(),s("Records")],1)],1)},n=[],r=s("2f62"),i=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("v-card",{staticClass:"mt-5"},[s("v-card-title",[e._v(" Showing past rounds for "+e._s(e.target_name)+" "),s("v-spacer"),s("archerSearch",{model:{value:e.archer,callback:function(t){e.archer=t},expression:"archer"}})],1),s("v-card-text",[s("v-data-table",{attrs:{dense:"","mobile-breakpoint":300,headers:e.p_table_header,items:e.p_table,"items-per-page":5,"multi-sort":""},scopedSlots:e._u([{key:"item.event",fn:function(t){return[e._v(" "+e._s(t.item.event)+" ("),s("router-link",{attrs:{to:{name:"event",params:{id:t.item.eId}}}},[e._v("link")]),e._v(") ")]}}])})],1)],1)},l=[],c=s("2151"),o=s("a676"),u={components:{archerSearch:c["a"]},data:()=>({archer:null,target_name:""}),watch:{archer:function(e){if(e&&e.events){this.target_name=this.archer.full_name,this.$store.dispatch("events/clearParticipants");for(let t of e.events)this.participants.find(e=>e.id===t)||this.$store.dispatch("events/getParticipant",t)}}},computed:{...Object(r["d"])({user:e=>e.user.user,participants:e=>e.events.participants,events:e=>e.events.events,courses:e=>e.courses.courses}),p_table_header(){return[{text:"Event",value:"event"},{text:"Date",value:"date",width:"120px"},{text:"Class",value:"class"},{text:"Course",value:"course"},{text:"Score",value:"score"}]},p_table(){let e=[];if(this.participants.length)for(let t of this.participants){let s=this.events.find(e=>e.id===t.event);if(s){let a=[];for(let n of t.scorecards){let r=s.rounds.find(e=>e.id===n.round),i=this.courses.find(e=>e.id===r.course),l=n.score,c=i.name;if("s"!==i.type){if("u"===i.type){let e=a.findIndex(e=>e.id===i.id);if(-1===e){a.push({id:i.id,score:l});continue}l=a[e].score+l,a.splice(e,1)}l&&e.push({eId:s.id,event:s.name,date:s.date_start,class:o["a"].getClass(t,s.ignore_gender),course:c.replace(/ (Round|Unit)( (Unm|M)arked Distances)? \(.*?\)/,"$2"),score:l})}}}}return e.sort((function(e,t){return e.date<t.date?1:e.date>t.date?-1:0}))}},created(){this.archer=this.user.archer,this.$store.dispatch("events/getEvents")}},d=u,h=s("2877"),p=s("6544"),f=s.n(p),m=s("b0af"),g=s("99d9"),v=s("8fea"),b=s("2fa4"),y=Object(h["a"])(d,i,l,!1,null,null,null),I=y.exports;f()(y,{VCard:m["a"],VCardText:g["c"],VCardTitle:g["d"],VDataTable:v["a"],VSpacer:b["a"]});var S=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("v-card",{staticClass:"mt-5"},[s("v-card-title",[e._v("Records "),s("v-spacer"),s("v-text-field",{attrs:{"append-icon":"mdi-magnify",label:"Filter","single-line":"","hide-details":""},model:{value:e.r_search,callback:function(t){e.r_search=t},expression:"r_search"}})],1),s("v-card-text",[s("v-row",[s("v-col",[s("v-select",{attrs:{dense:"",items:[{text:"--disabled--",value:null},{text:"Format",value:"format"},{text:"Class",value:"class"}],label:"organise archers by"},model:{value:e.group_by,callback:function(t){e.group_by=t},expression:"group_by"}})],1)],1),s("v-data-table",{attrs:{dense:"","mobile-breakpoint":300,headers:e.r_table_header,search:e.r_search,items:e.r_table,"items-per-page":50,"group-by":e.group_by,"multi-sort":""}})],1)],1)},x=[],_={components:{},data:()=>({r_search:"",format:{hunter:"IFAA Hunter",field:"IFAA Field",animal:"IFAA Animal (Marked distances)",flint:"IFAA Flint Indoor",indoor:"IFAA Indoor"},group_by:"format"}),computed:{...Object(r["d"])({records:e=>e.statistics.records}),r_table_header(){return[{text:"Format",value:"format"},{text:"Class",value:"class",width:"100px"},{text:"Score",value:"score"},{text:"Archer",value:"archer",width:"175px"},{text:"Event",value:"event"},{text:"national/EU/W",value:"scope"},{text:"Date",value:"date",width:"120px"}]},r_table(){return this.records.length?this.records.map(e=>Object.assign({class:e.age_group+e.gender+e.style},e,{format:this.format[e.format]})):[]}}},C=_,w=(s("d0d5"),s("62ad")),j=s("0fd9"),D=s("b974"),O=s("8654"),V=Object(h["a"])(C,S,x,!1,null,"5fb995eb",null),k=V.exports;f()(V,{VCard:m["a"],VCardText:g["c"],VCardTitle:g["d"],VCol:w["a"],VDataTable:v["a"],VRow:j["a"],VSelect:D["a"],VSpacer:b["a"],VTextField:O["a"]});var A={name:"Statistics",components:{ArcherPastEvents:I,Records:k},data:()=>({}),computed:{...Object(r["d"])({user:e=>e.user.user})}},F=A,$=s("a523"),T=s("a722"),M=Object(h["a"])(F,a,n,!1,null,null,null);t["default"]=M.exports;f()(M,{VCard:m["a"],VCardText:g["c"],VContainer:$["a"],VLayout:T["a"]})}}]);
//# sourceMappingURL=chunk-2bc8ebd0.2ef71186.js.map