// Peak normalization of a prepared selection. No MIDI, storage or source mutation.
export function normalizePeak(input,targetDb=-1){
 if(!Number.isFinite(targetDb)||targetDb>0||targetDb< -60)throw Error('Invalid normalization target');
 const pcm=Float32Array.from(input);let before=0;
 for(const x of pcm){if(!Number.isFinite(x))throw Error('Sample contains non-finite audio');before=Math.max(before,Math.abs(x));}
 const target=10**(targetDb/20),gain=before>1e-9?target/before:1;
 for(let i=0;i<pcm.length;i++)pcm[i]*=gain;
 return {pcm,before,after:before*gain,gain,gainDb:20*Math.log10(gain),silent:before<=1e-9};
}
