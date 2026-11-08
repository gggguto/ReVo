// GPL-3.0-only. Optional RAM-only Web MIDI transport. Caller selects/grants ports.
// This module never requests MIDI access, opens ports or sends update/boot commands.
import {response} from './protocol.mjs';
export class MidiSampleTransport{
 constructor(input,output,{timeoutMs=700,retries=3}={}){this.input=input;this.output=output;this.timeoutMs=timeoutMs;this.retries=retries;this.pending=null;this.closed=false;this.listener=e=>{let r;try{r=response(new Uint8Array(e.data));}catch{return;}const p=this.pending;if(p&&r.cmd===p.cmd&&r.sid===p.sid&&r.seq===p.seq){clearTimeout(p.timer);this.pending=null;p.resolve(r);}};input.addEventListener('midimessage',this.listener);}
 async request(wire){if(this.closed)throw Error('MIDI transport closed');if(this.pending)throw Error('MIDI request already pending');for(let i=0;i<this.retries;i++){try{return await new Promise((resolve,reject)=>{const p={cmd:wire[5],sid:wire[6]|wire[7]<<7,seq:wire[8]|wire[9]<<7,resolve,reject};p.timer=setTimeout(()=>{this.pending=null;reject(Error('MIDI reply timeout'));},this.timeoutMs);this.pending=p;try{this.output.send(wire);}catch(e){clearTimeout(p.timer);this.pending=null;reject(e);}});}catch(e){if(this.closed||i===this.retries-1)throw e;}}}
 close(){this.closed=true;this.input.removeEventListener('midimessage',this.listener);if(this.pending){clearTimeout(this.pending.timer);this.pending.reject(Error('MIDI transport closed'));this.pending=null;}}
}
