const chapter=document.querySelector('#edit'),image=chapter?.querySelector('[data-edit-screen]');
if(image){
 const notes={same:'With the same sample in both loops, both playback windows share the waveform. Red is Loop A; cyan is Loop B.','different-a':'With different samples, selecting Loop A shows only its sample and red playback window. Use ALGO on the instrument to select the other loop.','different-b':'With different samples, selecting Loop B shows only its sample and cyan playback window. Each loop keeps its own sample and playback settings.'};
 let mode='same',frame=0,visible=false;const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const path=()=>new URL(`../assets/screens/edit-${mode}-${String(frame).padStart(2,'0')}.png`,import.meta.url).href;
 new IntersectionObserver(e=>{visible=e[0].isIntersecting;}).observe(image);
 chapter.addEventListener('click',e=>{const b=e.target.closest('[data-edit-example]');if(!b)return;mode=b.dataset.editExample;frame=0;image.src=path();image.alt=notes[mode];chapter.querySelector('[data-edit-note]').textContent=notes[mode];for(const el of chapter.querySelectorAll('[data-edit-example]'))el.setAttribute('aria-pressed',String(el===b));});
 const timer=setInterval(()=>{if(visible&&!document.hidden&&!reduced.matches){frame=(frame+1)%36;image.src=path();}},80);addEventListener('pagehide',()=>clearInterval(timer),{once:true});
}
