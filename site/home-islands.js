// Replays captured native Home frames; no new movement paths or sprites.
const root=new URL('./assets/homes/',import.meta.url);const reduced=matchMedia('(prefers-reduced-motion: reduce)');
for(const image of document.querySelectorAll('[data-island-machine],[data-home-player]')){
 const machine=image.dataset.islandMachine||image.dataset.homePlayer,full=!!image.dataset.homePlayer,count=machine==='bioma'?24:35,period=machine==='bioma'?220:405;let visible=false,start=0,loaded=false;
 const frame=n=>new URL(`${machine}${full?'-full':''}-${String(n).padStart(2,'0')}.png`,root).href;
 const io=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible&&!loaded){loaded=true;for(let i=0;i<count;i++){const p=new Image();p.src=frame(i);}}});io.observe(image);
 const show=()=>{if(!visible||document.hidden||reduced.matches||full&&image.dataset.homeMode!=='play')return;image.src=frame(Math.floor((performance.now()-start)/period)%count);};
 const timer=setInterval(show,period);addEventListener('pagehide',()=>clearInterval(timer),{once:true});
 if(full){const chapter=image.closest('.chapter');for(const button of chapter.querySelectorAll('[data-home-status]'))button.addEventListener('click',()=>{const state=button.dataset.homeStatus;image.dataset.homeMode=state;start=performance.now();image.src=state==='play'?frame(0):new URL('bioma-stop.png',root).href;image.alt=`Bioma Home — ${state.toUpperCase()} status and grey page shortcuts`;for(const b of chapter.querySelectorAll('[data-home-status]'))b.setAttribute('aria-pressed',String(b===button));});}
}
