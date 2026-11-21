'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
function setup(mobile=true){
  const state={focus:null,scrolls:[],hash:''};
  const elements=[];
  function element(tag){
    const e={tag,children:[],style:{},dataset:{},events:{},attributes:{},
      append(child){this.children.push(child);},
      replaceChildren(){this.children=[];},
      setAttribute(k,v){this.attributes[k]=v;},
      addEventListener(k,f){this.events[k]=f;},
      focus(options){state.focus={element:this,options};},
      scrollIntoView(options){state.scrolls.push({element:this,options});},
      querySelector(selector){return this.children.find(c=>'#'+c.id===selector);}};
    Object.defineProperty(e,'href',{set(v){this.url=v;this.hash=v.startsWith('#')?v:'';},get(){return this.url;}});
    elements.push(e);return e;
  }
  const named=Object.fromEntries(['#evidence','#reading-list','#nodes','#edges','canvas'].map(id=>[id,element(id)]));
  named.canvas.getContext=()=>null;
  const document={querySelector:s=>named[s],createElement:element,
    querySelectorAll:s=>elements.filter(e=>s==='.edge'?e.className==='edge':['edge','node'].includes(e.className)),
    body:{classList:{add(){}}}};
  vm.runInNewContext(fs.readFileSync(require.resolve('./map.js'),'utf8'),{
    document,location:{hash:''},history:{replaceState(a,b,hash){state.hash=hash;}},
    window:{matchMedia:()=>({matches:mobile}),addEventListener(){}},
    ResizeObserver:class{observe(){}}});
  return {state,edges:elements.filter(e=>e.className==='edge'),panel:named['#evidence']};
}
function click(link,extra={}){
  let prevented=false;
  link.events.click({button:0,preventDefault(){prevented=true;},...extra});
  return prevented;
}
test('all mobile questions focus and reveal their answer, including repeat selection',()=>{
  const s=setup();assert.equal(s.state.focus,null);assert.equal(s.state.scrolls.length,0);
  for(const edge of [...s.edges,s.edges[0]]){
    assert.equal(click(edge),true);
    const heading=s.panel.querySelector('#evidence-title');
    assert.equal(heading.tabIndex,-1);assert.equal(s.state.focus.element,heading);
    assert.equal(s.state.focus.options.preventScroll,true);
    assert.equal(s.state.scrolls.at(-1).element,heading);
    assert.equal(s.state.scrolls.at(-1).options.behavior,'instant');
    assert.equal(edge.attributes['aria-current'],'true');
    assert.equal(s.state.hash,edge.hash);
  }
});
test('desktop selection focuses the answer without jumping the page',()=>{
  const s=setup(false);click(s.edges[1]);
  assert.equal(s.state.focus.element,s.panel.querySelector('#evidence-title'));
  assert.equal(s.state.scrolls.length,0);
});
test('modified and middle clicks retain native link behaviour',()=>{
  for(const extra of [{ctrlKey:true},{metaKey:true},{shiftKey:true},{altKey:true},{button:1}]){
    const s=setup();assert.equal(click(s.edges[1],extra),false);
    assert.equal(s.state.focus,null);assert.equal(s.state.scrolls.length,0);
  }
});
