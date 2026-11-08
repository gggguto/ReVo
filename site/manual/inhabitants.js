import {formatManual} from './format.js';
// Native LCD captures only. The tutorial switches examples, never device state.
const section=document.querySelector('#inhabitants');
if(section){
 const data=await(await fetch(new URL('./inhabitants.json',import.meta.url))).json(),image=section.querySelector('[data-inhabitant-screen]'),tabs=[...section.querySelectorAll('[data-inhabitant]')],modeButtons=[...section.querySelectorAll('button[data-timing]')],keys=['birds','insects','water'];
 let family=keys.includes(location.hash.slice(1))?location.hash.slice(1):'birds',mode='tame',started=performance.now(),visible=false;const loaded=new Set(),reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const path=n=>new URL(`../assets/screens/inhabitants-${family}-${mode}-${String(n).padStart(2,'0')}.png`,import.meta.url).href;
 function update(){
  const c=data[family];section.dataset.family=family;section.dataset.timing=mode;section.style.setProperty('--accent',c.color);document.documentElement.style.setProperty('--inhabitant-accent',c.color);section.querySelector('[data-inhabitant-description]').textContent=c.intro;
  section.querySelector('[role=tabpanel]').setAttribute('aria-labelledby','inhabitant-tab-'+family);
  for(const t of tabs){const on=t.dataset.inhabitant===family;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;}
  for(const b of modeButtons)b.setAttribute('aria-pressed',String(b.dataset.timing===mode));
  section.querySelector('[data-cycle-state]').textContent=mode==='tame'?'Cycle is active in Tame. It follows the global clock.':'In Wild, timing is free and Cycle rests. Switch to Tame to bring it onto the clock.';
  const list=section.querySelector('.inhabitant-controls');list.replaceChildren();
  for(const p of c.controls){const li=document.createElement('li'),strong=document.createElement('strong'),number=document.createElement('span'),body=document.createElement('p');li.tabIndex=0;li.setAttribute('role','button');li.setAttribute('aria-pressed','false');li.dataset.knob=String(p.n);number.className='number';number.textContent=p.n;strong.append(number,document.createTextNode(p.name));body.textContent=p.text;li.append(strong,body);list.append(li);}
  section.querySelector('[data-inhabitant-try]').textContent=c.tryit;section.querySelector('[data-inhabitant-extra]').textContent=c.extra;
  const knob=section.dataset.selectedKnob||'3';for(const el of section.querySelectorAll('[data-knob]')){const on=el.dataset.knob===knob;el.classList.toggle('active',on);if(el.matches('[role=button]'))el.setAttribute('aria-pressed',String(on));}
  started=performance.now();image.src=path(0);image.alt=`${c.label} — ${mode==='tame'?'Tame, with Cycle active':'Wild, with Cycle inactive'}`;
  formatManual(section);const pair=family+'-'+mode;if(!loaded.has(pair)){loaded.add(pair);for(let n=0;n<6;n++){const preload=new Image();preload.src=path(n);}}
 }
 tabs.forEach(t=>{t.addEventListener('click',()=>{family=t.dataset.inhabitant;update();});t.addEventListener('keydown',e=>{let at=keys.indexOf(family);if(e.key==='ArrowRight')at=(at+1)%3;else if(e.key==='ArrowLeft')at=(at+2)%3;else if(e.key==='Home')at=0;else if(e.key==='End')at=2;else return;e.preventDefault();family=keys[at];update();tabs[at].focus();});});
 modeButtons.forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.timing;update();}));
 addEventListener('hashchange',()=>{const next=location.hash.slice(1);if(keys.includes(next)){family=next;update();}});
 new IntersectionObserver(e=>visible=e[0].isIntersecting).observe(image);
 const timer=setInterval(()=>{if(visible&&!document.hidden&&!reduced.matches)image.src=path(Math.floor((performance.now()-started)/220)%6);},220);addEventListener('pagehide',()=>clearInterval(timer),{once:true});update();
}
