// SPDX-License-Identifier: GPL-3.0-only
// IMA encoder ported from SLOOP/Felucca tools/sampleio.py.
// Copyright (C) 2026 Leo Kuroshita, Hügelton Instruments.
const steps=[7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767],adjust=[-1, -1, -1, -1, 2, 4, 6, 8];
export function encodeIMA(pcm){
 const out=new Uint8Array(Math.ceil(pcm.length/2));let pred=0,idx=0;
 for(let n=0;n<pcm.length;n++){
  const x=Math.max(-32768,Math.min(32767,Math.round(pcm[n]*32768)));
  const step=steps[idx];let diff=x-pred,code=0;if(diff<0){code=8;diff=-diff;}
  let vd=step>>3;if(diff>=step){code|=4;diff-=step;vd+=step;}
  if(diff>=(step>>1)){code|=2;diff-=step>>1;vd+=step>>1;}
  if(diff>=(step>>2)){code|=1;vd+=step>>2;}
  pred=Math.max(-32768,Math.min(32767,pred+((code&8)?-vd:vd)));
  idx=Math.max(0,Math.min(88,idx+adjust[code&7]));out[n>>1]|=code<<((n&1)*4);
 }return out;
}
// ReVo preview decoder. Mirrors the firmware's low-nibble-first IMA step update.
export function decodeIMA(data,frames){
 if(!Number.isInteger(frames)||frames<0||frames>data.length*2)throw Error('Invalid ADPCM preview length');
 const pcm=new Float32Array(frames);let pred=0,idx=0;
 for(let n=0;n<frames;n++){const code=(data[n>>1]>>((n&1)*4))&15,step=steps[idx];let diff=step>>3;if(code&4)diff+=step;if(code&2)diff+=step>>1;if(code&1)diff+=step>>2;pred=Math.max(-32768,Math.min(32767,pred+((code&8)?-diff:diff)));idx=Math.max(0,Math.min(88,idx+adjust[code&7]));pcm[n]=pred/32768;}
 return pcm;
}
