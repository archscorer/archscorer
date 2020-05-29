(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-f434b53a"],{"0798":function(t,e,r){"use strict";r("caad");var n=r("5530"),a=r("ade3"),i=(r("0c18"),r("10d2")),o=r("afdd"),s=r("9d26"),c=r("f2e7"),l=r("7560"),u=r("2b0e"),d=u["a"].extend({name:"transitionable",props:{mode:String,origin:String,transition:String}}),f=r("58df"),h=r("d9bd");e["a"]=Object(f["a"])(i["a"],c["a"],d).extend({name:"v-alert",props:{border:{type:String,validator:function(t){return["top","right","bottom","left"].includes(t)}},closeLabel:{type:String,default:"$vuetify.close"},coloredBorder:Boolean,dense:Boolean,dismissible:Boolean,icon:{default:"",type:[Boolean,String],validator:function(t){return"string"===typeof t||!1===t}},outlined:Boolean,prominent:Boolean,text:Boolean,type:{type:String,validator:function(t){return["info","error","success","warning"].includes(t)}},value:{type:Boolean,default:!0}},computed:{__cachedBorder:function(){if(!this.border)return null;var t={staticClass:"v-alert__border",class:Object(a["a"])({},"v-alert__border--".concat(this.border),!0)};return this.coloredBorder&&(t=this.setBackgroundColor(this.computedColor,t),t.class["v-alert__border--has-color"]=!0),this.$createElement("div",t)},__cachedDismissible:function(){var t=this;if(!this.dismissible)return null;var e=this.iconColor;return this.$createElement(o["a"],{staticClass:"v-alert__dismissible",props:{color:e,icon:!0,small:!0},attrs:{"aria-label":this.$vuetify.lang.t(this.closeLabel)},on:{click:function(){return t.isActive=!1}}},[this.$createElement(s["a"],{props:{color:e}},"$cancel")])},__cachedIcon:function(){return this.computedIcon?this.$createElement(s["a"],{staticClass:"v-alert__icon",props:{color:this.iconColor}},this.computedIcon):null},classes:function(){var t=Object(n["a"])(Object(n["a"])({},i["a"].options.computed.classes.call(this)),{},{"v-alert--border":Boolean(this.border),"v-alert--dense":this.dense,"v-alert--outlined":this.outlined,"v-alert--prominent":this.prominent,"v-alert--text":this.text});return this.border&&(t["v-alert--border-".concat(this.border)]=!0),t},computedColor:function(){return this.color||this.type},computedIcon:function(){return!1!==this.icon&&("string"===typeof this.icon&&this.icon?this.icon:!!["error","info","success","warning"].includes(this.type)&&"$".concat(this.type))},hasColoredIcon:function(){return this.hasText||Boolean(this.border)&&this.coloredBorder},hasText:function(){return this.text||this.outlined},iconColor:function(){return this.hasColoredIcon?this.computedColor:void 0},isDark:function(){return!(!this.type||this.coloredBorder||this.outlined)||l["a"].options.computed.isDark.call(this)}},created:function(){this.$attrs.hasOwnProperty("outline")&&Object(h["a"])("outline","outlined",this)},methods:{genWrapper:function(){var t=[this.$slots.prepend||this.__cachedIcon,this.genContent(),this.__cachedBorder,this.$slots.append,this.$scopedSlots.close?this.$scopedSlots.close({toggle:this.toggle}):this.__cachedDismissible],e={staticClass:"v-alert__wrapper"};return this.$createElement("div",e,t)},genContent:function(){return this.$createElement("div",{staticClass:"v-alert__content"},this.$slots.default)},genAlert:function(){var t={staticClass:"v-alert",attrs:{role:"alert"},class:this.classes,style:this.styles,directives:[{name:"show",value:this.isActive}]};if(!this.coloredBorder){var e=this.hasText?this.setTextColor:this.setBackgroundColor;t=e(this.computedColor,t)}return this.$createElement("div",t,[this.genWrapper()])},toggle:function(){this.isActive=!this.isActive}},render:function(t){var e=this.genAlert();return this.transition?t("transition",{props:{name:this.transition,origin:this.origin,mode:this.mode}},[e]):e}})},"0c18":function(t,e,r){},"0fd9":function(t,e,r){"use strict";r("99af"),r("4160"),r("caad"),r("13d5"),r("4ec9"),r("b64b"),r("d3b7"),r("ac1f"),r("2532"),r("3ca3"),r("5319"),r("159b"),r("ddb0");var n=r("ade3"),a=r("5530"),i=(r("4b85"),r("2b0e")),o=r("d9f7"),s=r("80d2"),c=["sm","md","lg","xl"],l=["start","end","center"];function u(t,e){return c.reduce((function(r,n){return r[t+Object(s["D"])(n)]=e(),r}),{})}var d=function(t){return[].concat(l,["baseline","stretch"]).includes(t)},f=u("align",(function(){return{type:String,default:null,validator:d}})),h=function(t){return[].concat(l,["space-between","space-around"]).includes(t)},p=u("justify",(function(){return{type:String,default:null,validator:h}})),v=function(t){return[].concat(l,["space-between","space-around","stretch"]).includes(t)},b=u("alignContent",(function(){return{type:String,default:null,validator:v}})),m={align:Object.keys(f),justify:Object.keys(p),alignContent:Object.keys(b)},g={align:"align",justify:"justify",alignContent:"align-content"};function y(t,e,r){var n=g[t];if(null!=r){if(e){var a=e.replace(t,"");n+="-".concat(a)}return n+="-".concat(r),n.toLowerCase()}}var _=new Map;e["a"]=i["a"].extend({name:"v-row",functional:!0,props:Object(a["a"])(Object(a["a"])(Object(a["a"])({tag:{type:String,default:"div"},dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:d}},f),{},{justify:{type:String,default:null,validator:h}},p),{},{alignContent:{type:String,default:null,validator:v}},b),render:function(t,e){var r=e.props,a=e.data,i=e.children,s="";for(var c in r)s+=String(r[c]);var l=_.get(s);return l||function(){var t,e;for(e in l=[],m)m[e].forEach((function(t){var n=r[t],a=y(e,t,n);a&&l.push(a)}));l.push((t={"no-gutters":r.noGutters,"row--dense":r.dense},Object(n["a"])(t,"align-".concat(r.align),r.align),Object(n["a"])(t,"justify-".concat(r.justify),r.justify),Object(n["a"])(t,"align-content-".concat(r.alignContent),r.alignContent),t)),_.set(s,l)}(),t(r.tag,Object(o["a"])(a,{staticClass:"row",class:l}),i)}})},"4bd4":function(t,e,r){"use strict";r("4de4"),r("7db0"),r("4160"),r("caad"),r("07ac"),r("2532"),r("159b");var n=r("5530"),a=r("58df"),i=r("7e2b"),o=r("3206");e["a"]=Object(a["a"])(i["a"],Object(o["b"])("form")).extend({name:"v-form",inheritAttrs:!1,props:{lazyValidation:Boolean,value:Boolean},data:function(){return{inputs:[],watchers:[],errorBag:{}}},watch:{errorBag:{handler:function(t){var e=Object.values(t).includes(!0);this.$emit("input",!e)},deep:!0,immediate:!0}},methods:{watchInput:function(t){var e=this,r=function(t){return t.$watch("hasError",(function(r){e.$set(e.errorBag,t._uid,r)}),{immediate:!0})},n={_uid:t._uid,valid:function(){},shouldValidate:function(){}};return this.lazyValidation?n.shouldValidate=t.$watch("shouldValidate",(function(a){a&&(e.errorBag.hasOwnProperty(t._uid)||(n.valid=r(t)))})):n.valid=r(t),n},validate:function(){return 0===this.inputs.filter((function(t){return!t.validate(!0)})).length},reset:function(){this.inputs.forEach((function(t){return t.reset()})),this.resetErrorBag()},resetErrorBag:function(){var t=this;this.lazyValidation&&setTimeout((function(){t.errorBag={}}),0)},resetValidation:function(){this.inputs.forEach((function(t){return t.resetValidation()})),this.resetErrorBag()},register:function(t){this.inputs.push(t),this.watchers.push(this.watchInput(t))},unregister:function(t){var e=this.inputs.find((function(e){return e._uid===t._uid}));if(e){var r=this.watchers.find((function(t){return t._uid===e._uid}));r&&(r.valid(),r.shouldValidate()),this.watchers=this.watchers.filter((function(t){return t._uid!==e._uid})),this.inputs=this.inputs.filter((function(t){return t._uid!==e._uid})),this.$delete(this.errorBag,e._uid)}}},render:function(t){var e=this;return t("form",{staticClass:"v-form",attrs:Object(n["a"])({novalidate:!0},this.attrs$),on:{submit:function(t){return e.$emit("submit",t)}}},this.$slots.default)}})},"62ad":function(t,e,r){"use strict";r("4160"),r("caad"),r("13d5"),r("45fc"),r("4ec9"),r("a9e3"),r("b64b"),r("d3b7"),r("ac1f"),r("3ca3"),r("5319"),r("2ca0"),r("159b"),r("ddb0");var n=r("ade3"),a=r("5530"),i=(r("4b85"),r("2b0e")),o=r("d9f7"),s=r("80d2"),c=["sm","md","lg","xl"],l=function(){return c.reduce((function(t,e){return t[e]={type:[Boolean,String,Number],default:!1},t}),{})}(),u=function(){return c.reduce((function(t,e){return t["offset"+Object(s["D"])(e)]={type:[String,Number],default:null},t}),{})}(),d=function(){return c.reduce((function(t,e){return t["order"+Object(s["D"])(e)]={type:[String,Number],default:null},t}),{})}(),f={col:Object.keys(l),offset:Object.keys(u),order:Object.keys(d)};function h(t,e,r){var n=t;if(null!=r&&!1!==r){if(e){var a=e.replace(t,"");n+="-".concat(a)}return"col"!==t||""!==r&&!0!==r?(n+="-".concat(r),n.toLowerCase()):n.toLowerCase()}}var p=new Map;e["a"]=i["a"].extend({name:"v-col",functional:!0,props:Object(a["a"])(Object(a["a"])(Object(a["a"])(Object(a["a"])({cols:{type:[Boolean,String,Number],default:!1}},l),{},{offset:{type:[String,Number],default:null}},u),{},{order:{type:[String,Number],default:null}},d),{},{alignSelf:{type:String,default:null,validator:function(t){return["auto","start","end","center","baseline","stretch"].includes(t)}},tag:{type:String,default:"div"}}),render:function(t,e){var r=e.props,a=e.data,i=e.children,s=(e.parent,"");for(var c in r)s+=String(r[c]);var l=p.get(s);return l||function(){var t,e;for(e in l=[],f)f[e].forEach((function(t){var n=r[t],a=h(e,t,n);a&&l.push(a)}));var a=l.some((function(t){return t.startsWith("col-")}));l.push((t={col:!a||!r.cols},Object(n["a"])(t,"col-".concat(r.cols),r.cols),Object(n["a"])(t,"offset-".concat(r.offset),r.offset),Object(n["a"])(t,"order-".concat(r.order),r.order),Object(n["a"])(t,"align-self-".concat(r.alignSelf),r.alignSelf),t)),p.set(s,l)}(),t(r.tag,Object(o["a"])(a,{class:l}),i)}})},"6b70":function(t,e,r){"use strict";r.r(e);var n=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("v-row",{attrs:{justify:"center"}},[r("v-col",{attrs:{cols:"12",sm:"10",md:"8",lg:"6"}},[r("v-alert",{staticClass:"text-justify",attrs:{type:"warning",outlined:""}},[t._v(" For new user associated archer profile is selected based on account email address from our database, if one or more exists. If there is more than one archer profile associated with given email address (contact email for many archers), first (random?) one is bound to given user account. Currently you have "),r("b",[t._v("no")]),t._v(" way to change that on your own and "),r("b",[t._v("please don't change existing profile, if its intended to somebody else")]),t._v(". Contact 'info @ archscorer . faae . ee' to reassign correct profile to your account. ")]),r("v-card",[r("v-card-title",[r("span",{staticClass:"headline"},[t._v("Archer Profile")])]),r("v-form",[r("v-container",[r("v-row",[r("v-col",{attrs:{cols:"4"}},[r("v-text-field",{attrs:{autofocus:"",label:"Your full name",hint:"Your full name can not be empty string!"},model:{value:t.user.archer.full_name,callback:function(e){t.$set(t.user.archer,"full_name",e)},expression:"user.archer.full_name"}})],1),r("v-col",{attrs:{cols:"4"}},[r("v-select",{attrs:{items:[{text:"Male",value:"M"},{text:"Female",value:"F"}],label:"Gender"},model:{value:t.user.archer.gender,callback:function(e){t.$set(t.user.archer,"gender",e)},expression:"user.archer.gender"}})],1),r("v-col",{attrs:{cols:"4"}},[r("v-select",{attrs:{items:t.clubs?t.clubs:[],label:"Choose Club","item-text":"name","item-value":"id"},model:{value:t.user.archer.club,callback:function(e){t.$set(t.user.archer,"club",e)},expression:"user.archer.club"}})],1)],1),r("v-row",[r("v-col",{attrs:{cols:"4"}},[r("v-text-field",{attrs:{label:"Contact email address"},model:{value:t.user.archer.email,callback:function(e){t.$set(t.user.archer,"email",e)},expression:"user.archer.email"}})],1),r("v-col",{attrs:{cols:"4"}},[r("v-text-field",{attrs:{label:"Contact phone number"},model:{value:t.user.archer.phone,callback:function(e){t.$set(t.user.archer,"phone",e)},expression:"user.archer.phone"}})],1),r("v-col",{attrs:{cols:"4"}},[r("v-text-field",{attrs:{label:"Archer national ID",hint:"FAAE ID in Estonia - first 7 digits from your national ID code."},model:{value:t.user.archer.nat_id,callback:function(e){t.$set(t.user.archer,"nat_id",e)},expression:"user.archer.nat_id"}})],1)],1)],1)],1),r("v-card-actions",[r("v-spacer"),r("v-btn",{attrs:{color:"primary"},on:{click:function(e){t.putArcher(t.user.archer),t.$router.go(-1)}}},[t._v("Save")])],1)],1)],1)],1)},a=[],i=r("5530"),o=r("2f62"),s={data:function(){return{}},computed:Object(i["a"])({},Object(o["c"])({user:function(t){return t.user.user},clubs:function(t){return t.clubs.clubs}})),methods:Object(i["a"])({},Object(o["b"])("user",["putArcher"])),created:function(){this.$store.dispatch("clubs/getClubs")}},c=s,l=r("2877"),u=r("6544"),d=r.n(u),f=r("0798"),h=r("8336"),p=r("b0af"),v=r("99d9"),b=r("62ad"),m=r("a523"),g=r("4bd4"),y=r("0fd9"),_=r("b974"),j=r("2fa4"),C=r("8654"),w=Object(l["a"])(c,n,a,!1,null,null,null);e["default"]=w.exports;d()(w,{VAlert:f["a"],VBtn:h["a"],VCard:p["a"],VCardActions:v["a"],VCardTitle:v["d"],VCol:b["a"],VContainer:m["a"],VForm:g["a"],VRow:y["a"],VSelect:_["a"],VSpacer:j["a"],VTextField:C["a"]})}}]);
//# sourceMappingURL=chunk-f434b53a.cc94c111.js.map