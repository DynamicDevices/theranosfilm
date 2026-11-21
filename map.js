/* Curated prototype only. Never import the private working dataset here. */
'use strict';
const topics = [
  {id:'promise',title:'The promise',kind:'Claim',x:.12,y:.18},
  {id:'deck',title:'Investor presentation',kind:'Trial exhibit 3696',x:.52,y:.18},
  {id:'investors',title:'Investor disclosures',kind:'Legal evidence',x:.88,y:.42},
  {id:'technology',title:'The technology',kind:'Research question',x:.12,y:.78},
  {id:'patents',title:'Patents & IPR',kind:'Patent record',x:.52,y:.84},
  {id:'film',title:'The film',kind:'Scene comparison pending',x:.88,y:.82}
];
const exhibit = 'https://files.cand.uscourts.gov/files/18-CR-258%20USA%20v.%20Holmes/Trial%20Exh.%203696/Trial%20Exh.%203696%20Presentation.pdf';
const links = [
  {id:'claim-deck',a:'promise',b:'deck',label:'What was claimed?',status:'Document wording',title:'A present-tense technology claim',text:'Page 3 of trial Exhibit 3696 describes proprietary, patented technology that “runs comprehensive blood tests from a finger-stick”. This is evidence of what this document says.',limit:'The wording does not establish clinical performance, who received this version, when they received it or what qualifications accompanied it. Page-level review is not a complete audit of the presentation.',source:exhibit,sourceLabel:'Read Exhibit 3696 · page 3'},
  {id:'deck-investors',a:'deck',b:'investors',label:'What was disclosed?',status:'SEC allegation',title:'The investor information package',text:'Paragraphs 48–51 of the SEC’s 2018 complaint describe investor meetings, demonstrations and materials including slides, reports and financial forecasts.',limit:'A complaint contains allegations, not findings on every statement. Establishing a particular investor’s knowledge requires the actual materials, delivery history and testimony.',source:'https://www.sec.gov/files/litigation/complaints/2018/comp-pr2018-41-theranos-holmes.pdf',sourceLabel:'Read the SEC complaint · paragraphs 48–51'},
  {id:'promise-technology',a:'promise',b:'technology',label:'Did it work then?',status:'Open question',title:'Capability now versus future potential',text:'The investigation must separate a working laboratory result from an aspiration, and an individual assay from the claimed breadth of a platform.',limit:'No clinical validation finding is made by this prototype. The investor presentation is a claim to test, not independent experimental confirmation.',source:exhibit,sourceLabel:'Inspect the claimed capability · Exhibit 3696'},
  {id:'technology-patents',a:'technology',b:'patents',label:'What was protected?',status:'Patent record',title:'A patent is not a performance certificate',text:'US8283155B2 is a starting point for investigating point-of-care fluidic systems. Its claims must be compared with the actual devices and the capabilities represented to investors.',limit:'Patent publication or grant does not establish clinical accuracy, commercial readiness, ownership today or that an investor saw this patent. A full claim and ownership audit remains unfinished.',source:'https://patents.google.com/patent/US8283155B2/en',sourceLabel:'Read patent US8283155B2'},
  {id:'film-investors',a:'investors',b:'film',label:'How does the film compare?',status:'Comparison pending',title:'Compare a scene with its underlying evidence',text:'Each film assertion needs a scene reference, exact wording, speaker, recording context and a comparison with contemporaneous documents.',limit:'No scene has been authenticated for this public prototype. Viewer recollection and third-party transcripts must not be presented as verified footage.',source:null,sourceLabel:null}
];
const byId = Object.fromEntries(topics.map(t => [t.id,t]));
const panel = document.querySelector('#evidence');
const researchTargets = {'claim-deck':'claims.html#claim-now','deck-investors':'timeline.html',
  'promise-technology':'claims.html#claim-platform','technology-patents':'claims.html#claim-patent',
  'film-investors':'film-guide.html#sequence-investors'};
function content(link, container, full) {
  container.replaceChildren();
  const add = (tag, text, cls) => {const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;container.append(e);return e;};
  add('p',link.status,'status');
  const heading=add(full?'h2':'h3',link.title);if(full)heading.id='evidence-title';
  add('p',link.text);
  add('h3','What this does not establish');add('p',link.limit,'limit');
  if(link.source){const a=add('a',link.sourceLabel);a.href=link.source;}
  if(researchTargets[link.id]){const p=add('p','');const a=document.createElement('a');a.href=researchTargets[link.id];a.textContent='Follow this question into the analysis';p.append(a);}
}
let selected=links[0].id;
// Replace the server-readable fallback only after the interactive script runs.
document.querySelector('#reading-list').replaceChildren();
function select(id){const link=links.find(l=>l.id===id);if(!link)return;selected=id;content(link,panel,true);document.querySelectorAll('.edge').forEach(a=>a.setAttribute('aria-current',String(a.dataset.id===id)));draw();}
for(const t of topics){const a=document.createElement('a');a.className='node';a.href='#'+links.find(l=>l.a===t.id||l.b===t.id).id;a.style.left=t.x*100+'%';a.style.top=t.y*100+'%';a.textContent=t.title;const small=document.createElement('small');small.textContent=t.kind;a.append(small);document.querySelector('#nodes').append(a);}
for(const l of links){const a=document.createElement('a');a.className='edge';a.dataset.id=l.id;a.href='#'+l.id;a.textContent=l.label;a.style.left=(byId[l.a].x+byId[l.b].x)*50+'%';a.style.top=(byId[l.a].y+byId[l.b].y)*50+'%';document.querySelector('#edges').append(a);const article=document.createElement('article');article.id=l.id;content(l,article,false);document.querySelector('#reading-list').append(article);}
// Native anchors retain a readable destination if graphics are unavailable.
document.querySelectorAll('.edge,.node').forEach(a=>a.addEventListener('click',event=>{
  // A normal selection updates the source panel in place. Modified clicks retain
  // native link behaviour; the same anchors still work without JavaScript.
  if(event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
  event.preventDefault();
  history.replaceState(null,'',a.hash);
  select(a.hash.slice(1));
}));
window.addEventListener('hashchange',()=>select(location.hash.slice(1)));
const canvas=document.querySelector('canvas');
const gl=canvas.getContext('webgl');
let program, buffer, position, colour;
if(gl){
  try{
    const shader=(kind,source)=>{const s=gl.createShader(kind);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error('Shader failed');return s;};
    program=gl.createProgram();gl.attachShader(program,shader(gl.VERTEX_SHADER,'attribute vec2 p; void main(){gl_Position=vec4(p,0.0,1.0);}'));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,'precision mediump float; uniform vec4 c; void main(){gl_FragColor=c;}'));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error('Program failed');
    buffer=gl.createBuffer();position=gl.getAttribLocation(program,'p');colour=gl.getUniformLocation(program,'c');
  }catch{document.body.classList.add('no-webgl');program=null;}
}else document.body.classList.add('no-webgl');
function draw(){
  if(!gl||!program||gl.isContextLost())return;
  const ratio=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.round(canvas.clientWidth*ratio);canvas.height=Math.round(canvas.clientHeight*ratio);gl.viewport(0,0,canvas.width,canvas.height);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.useProgram(program);gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.enableVertexAttribArray(position);gl.vertexAttribPointer(position,2,gl.FLOAT,false,0,0);
  for(const l of links){const a=byId[l.a],b=byId[l.b];gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([a.x*2-1,1-a.y*2,b.x*2-1,1-b.y*2]),gl.STATIC_DRAW);gl.uniform4f(colour,...(selected===l.id?[.71,.07,.15,1]:[.66,.63,.61,1]));gl.drawArrays(gl.LINES,0,2);}
}
canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();document.body.classList.add('no-webgl');});
new ResizeObserver(draw).observe(canvas);
select(links.some(l=>l.id===location.hash.slice(1))?location.hash.slice(1):selected);
