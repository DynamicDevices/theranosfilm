'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const {createHeroMotion} = require('./hero-motion.js');
function setup(reduced=false, saveData=false) {
  const element = () => ({hidden:true,events:{},addEventListener(n,f){this.events[n]=f;}});
  const video = Object.assign(element(), {dataset:{src:'hero-loop.mp4'},src:'',
    plays:0,pauses:0,play(){this.plays++;return Promise.resolve();},pause(){this.pauses++;}});
  const poster=element(), button=element(), doc=Object.assign(element(),{hidden:false});
  poster.hidden=false;
  const preference=Object.assign(element(),{matches:reduced});
  let intersection;
  createHeroMotion(video,poster,button,preference,doc,{saveData},f=>{intersection=f;return {observe(){}};});
  return {video,poster,button,doc,preference,intersect:v=>intersection([{isIntersecting:v}])};
}
test('reduced motion and Save-Data do not attach a video source',()=>{
  for(const state of [setup(true),setup(false,true)]){
    assert.equal(state.video.src,'');assert.equal(state.video.plays,0);
    assert.equal(state.poster.hidden,false);
  }
});
test('explicit play opts into motion; poster stays until actual playback',()=>{
  const s=setup(true);s.button.events.click();
  assert.equal(s.video.src,'hero-loop.mp4');assert.equal(s.poster.hidden,false);
  s.video.events.playing();assert.equal(s.poster.hidden,true);
});
test('manual pause survives visibility and viewport changes',()=>{
  const s=setup();s.button.events.click();const plays=s.video.plays;
  s.doc.hidden=true;s.doc.events.visibilitychange();s.doc.hidden=false;s.doc.events.visibilitychange();
  s.intersect(false);s.intersect(true);
  assert.equal(s.video.plays,plays);assert.equal(s.button.textContent,'Play background video');
});
test('hidden or offscreen media pauses, then resumes when allowed',()=>{
  const s=setup();const plays=s.video.plays;s.intersect(false);s.intersect(true);
  assert.ok(s.video.pauses>0);assert.equal(s.video.plays,plays+1);
});
test('failure preserves poster and removes unusable control',()=>{
  const s=setup();s.video.events.error();
  assert.equal(s.poster.hidden,false);assert.equal(s.video.hidden,true);assert.equal(s.button.hidden,true);
});
test('autoplay rejection keeps a still and offers play',async()=>{
  const s=setup();s.video.play=()=>Promise.reject(new Error('blocked'));
  s.doc.events.visibilitychange();await Promise.resolve();
  assert.equal(s.poster.hidden,false);assert.equal(s.button.textContent,'Play background video');
});
