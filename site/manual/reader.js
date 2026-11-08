import './edit-views.js';
import './home-controls.js';
import './fragments.js';
import './screens.js';
import './inhabitants.js';
// Controls only highlight explanations. They do not access the FM-1.
for(const section of document.querySelectorAll('.chapter')){
 const select=n=>{section.dataset.selectedKnob=n;for(const el of section.querySelectorAll('[data-knob]')){const active=el.dataset.knob===n;el.classList.toggle('active',active);if(el.matches('[role=button]'))el.setAttribute('aria-pressed',String(active));}};
 section.addEventListener('click',e=>{const el=e.target.closest('[data-knob]');if(el&&section.contains(el))select(el.dataset.knob);});
 section.addEventListener('keydown',e=>{const el=e.target.closest('[role=button][data-knob]');if(el&&(e.key==='Enter'||e.key===' ')){e.preventDefault();select(el.dataset.knob);}});
}
const nav=[...document.querySelectorAll('.toc a')];const watch=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){for(const a of nav){const active=a.hash==='#'+e.target.id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');}}},{rootMargin:'-24px 0px -60% 0px',threshold:0});document.querySelectorAll('.chapter').forEach(x=>watch.observe(x));
document.fonts.ready.then(()=>{const id=decodeURIComponent(location.hash.slice(1));if(id)document.getElementById(id)?.scrollIntoView({block:'start',behavior:'instant'});});
