// An illustrative LCD value window, scoped to Atolls Home only.
const home=document.querySelector('#welcome .home-lcd-demo');
if(home){
 const chapter=home.closest('.chapter'),popup=home.querySelector('.home-value-popup');
 const values={'1':'Start 20%','2':'Size 30%','3':'Speed 1.00×','4':'Level 75%'};let timeout;
 chapter.addEventListener('click',event=>{const control=event.target.closest('[data-knob]');if(!control||!chapter.contains(control))return;const value=values[control.dataset.knob];if(!value)return;clearTimeout(timeout);popup.textContent=value;popup.hidden=false;timeout=setTimeout(()=>{popup.hidden=true;},2400);});
}
