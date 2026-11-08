// Play the real LCD sequences, with the firmware's original capture timing.
const definitions={distance:[48,400],drift:[48,300],beam:[47,150],resonance:[48,180],'atolls-glitch':[48,100]},reduced=matchMedia('(prefers-reduced-motion: reduce)');
for(const image of document.querySelectorAll('[data-native-sequence]')){
 const name=image.dataset.nativeSequence,[count,period]=definitions[name];let visible=false,loaded=false,start=performance.now();
 const path=n=>new URL(`../assets/screens/motion-${name}-${String(n).padStart(2,'0')}.png`,import.meta.url).href;
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible&&!loaded){loaded=true;start=performance.now();if(!reduced.matches)for(let n=0;n<count;n++){const p=new Image();p.src=path(n);}}}).observe(image);
 const timer=setInterval(()=>{if(visible&&!document.hidden&&!reduced.matches)image.src=path(Math.floor((performance.now()-start)/period)%count);},period);addEventListener('pagehide',()=>clearInterval(timer),{once:true});
}
