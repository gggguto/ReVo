import {formatManual} from './format.js';
const guide=document.querySelector('#fragments-keyboard');
if(guide){
 const keys=await(await fetch(new URL('./fragment-map.json',import.meta.url))).json(),buttons=[...guide.querySelectorAll('[data-fragment-key]')];
 function select(index){const k=keys[index];for(const b of buttons)b.setAttribute('aria-pressed',String(Number(b.dataset.fragmentKey)===index));guide.style.setProperty('--accent',k.bank==='A'?'var(--red)':k.bank==='B'?'var(--cyan)':'var(--ink)');guide.querySelector('[data-fragment-title]').textContent=(k.bank==='divider'?'Centre':`Loop ${k.bank}`)+` / ${k.note} — ${k.label}`;let text;
  if(k.action===13)text='This illuminated F#4 separates the two banks. It is silent and does not trigger a Fragment.';
  else if(k.action===8)text='Temporarily reverse the current direction. Hold this key with another Fragment to keep its division while reversing it. If the loop is stopped, Reverse alone prepares the direction; press a Fragment to start the sound.';
  else if(k.action===9)text='Half: play at half this loop’s current Speed while the key is held. Release it to leave the gesture through the configured Fragment Release.';
  else if(k.action===10)text='Double: play at twice this loop’s current Speed while held. The gesture keeps this bank’s routing and Fragment envelope.';
  else if(k.action===11||k.action===12)text=`${k.label}: repeat on ${k.action===11?'eighth':'sixteenth'}-note triplet timing, following the global clock tempo. Hold Reverse at the same time to invert its direction without changing the timing.`;
  else text=`${k.label}: repeat a slice on this musical note division, using the global clock tempo. The white keys become progressively shorter from left to right. Hold Reverse to invert the Fragment without changing its division.`;
  guide.querySelector('[data-fragment-description]').textContent=text;formatManual(guide.querySelector('.fragment-key-detail'));
 }
 for(const b of buttons){b.addEventListener('click',()=>select(Number(b.dataset.fragmentKey)));b.addEventListener('keydown',e=>{let n=Number(b.dataset.fragmentKey);if(e.key==='ArrowRight')n=(n+1)%27;else if(e.key==='ArrowLeft')n=(n+26)%27;else return;e.preventDefault();select(n);buttons[n].focus();});}select(1);
}
