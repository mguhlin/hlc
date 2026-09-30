(() => {
 'use strict';
 const data=JSON.parse(document.querySelector('#calendarData').textContent), L=data.labels;
 const $=id=>document.getElementById(id);
 const count=data.modules.length*5, page=$('calendarPage');
 let index=0,band='g35',dates=[],monthDate=null,timerLeft=300,timerId=null,animationId=null,projecting=false;
 const defaults={start:'2026-08-17',excluded:[]};
 const read=(k,f)=>{try{return JSON.parse(localStorage.getItem(k))??f;}catch{return f;}};
 const save=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v));}catch{/* Preferences are optional. */}};
 const utc=date=>new Date(date+'T12:00:00Z');
 const key=d=>d.toISOString().slice(0,10);
 const valid=s=>/^\d{4}-\d{2}-\d{2}$/.test(s)&&!Number.isNaN(utc(s).getTime())&&key(utc(s))===s&&Number(s.slice(0,4))>=1900&&Number(s.slice(0,4))<=2100;
 const todayKey=()=>{const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;};
 const format=(d,options)=>new Intl.DateTimeFormat(data.lang,{...options,timeZone:'UTC'}).format(d);
 let config=read('hlc-calendar',defaults);
 if(!config||!valid(config.start)||!Array.isArray(config.excluded)||config.excluded.length>1000||config.excluded.some(x=>!valid(x)))config={...defaults};
 const storedBand=read('hlc-grade','g35');if(data.bands.includes(storedBand))band=storedBand;
 $('gradeSelect').value=band;
 function buildDates(){dates=[];const excluded=new Set(config.excluded);let d=utc(config.start);while(dates.length<count){const weekday=d.getUTCDay();if(weekday!==0&&weekday!==6&&!excluded.has(key(d)))dates.push(new Date(d));d.setUTCDate(d.getUTCDate()+1);} }
 function hashIndex(){const h=location.hash.slice(1);if(/^day-\d+$/.test(h)){const n=Number(h.slice(4));if(n>=1&&n<=count)return n-1;}if(/^\d+$/.test(h)){const n=Number(h);if(n>=1&&n<=count)return n-1;}if(valid(h)){const i=dates.findIndex(d=>key(d)===h);if(i>=0)return i;}return null;}
 function nearest(){const t=utc(todayKey()).getTime();let i=0,best=Infinity;dates.forEach((d,n)=>{const diff=Math.abs(d.getTime()-t);if(diff<best){best=diff;i=n;}});return i;}
 function resetTimer(){if(timerId)clearInterval(timerId);timerId=null;timerLeft=300;$('timer').textContent='5:00';$('timerBtn').textContent=L.timerStart;$('timerBtn').setAttribute('aria-pressed','false');}
 function render(direction='',updateHash=true){
   resetTimer();
   const m=data.modules[Math.floor(index/5)],d=index%5,date=dates[index];
   if(animationId)clearTimeout(animationId);page.classList.remove('turn-next','turn-prev');
   if(direction){void page.offsetWidth;page.classList.add('turn-'+direction);animationId=setTimeout(()=>page.classList.remove('turn-next','turn-prev'),360);}
   $('dateHeading').textContent=format(date,{weekday:'long',month:'long',day:'numeric',year:'numeric'});
   $('dateNumber').textContent=format(date,{day:'2-digit'});
   $('subDate').textContent=`${L.day} ${index+1} / ${count} · ${L.week} ${Math.floor(index/5)+1}`;
   $('phaseLabel').textContent=L[data.phases[d]];
   $('activityTitle').textContent=m.title;
   $('stimulus').innerHTML=m.stimulus;
   $('taskText').textContent=data.tasks[m.kind][d];
   $('bandTask').textContent=L[band+'Task'];
   $('answerText').innerHTML=m.check;
   $('alignmentText').innerHTML=m.alignment;
   $('activityLink').href=m.activityUrl;
   $('checkDetails').open=false;$('teacherDetails').open=false;
   $('counter').textContent=`${L.day} ${index+1} / ${count} · ${L[band]}`;
   $('prevBtn').disabled=index===0;$('nextBtn').disabled=index===count-1;
   $('dayJump').value=index+1;
   if(updateHash)history.replaceState(null,'','#day-'+(index+1));
   $('live').textContent=`${L.day} ${index+1}. ${m.title}. ${L[data.phases[d]]}. ${L[band]}.`;
   document.title=`${L.day} ${index+1} · ${m.title} · ${L.site}`;
 }
 function go(n){const next=Math.max(0,Math.min(count-1,n));if(next===index)return;const dir=next<index?'prev':'next';index=next;$('dateNotice').hidden=true;render(dir);}
 function showToday(){index=nearest();$('dateNotice').textContent=L.nearest;$('dateNotice').hidden=key(dates[index])===todayKey();render();}
 function drawMonth(){
   const grid=$('monthGrid');grid.replaceChildren();$('weekdays').replaceChildren();
   for(let i=0;i<7;i++){const cell=document.createElement('span');cell.textContent=format(new Date(Date.UTC(2026,10,1+i,12)),{weekday:'short'});$('weekdays').append(cell);}
   $('monthLabel').textContent=format(monthDate,{month:'long',year:'numeric'});
   const year=monthDate.getUTCFullYear(),month=monthDate.getUTCMonth();
   const first=new Date(Date.UTC(year,month,1,12)),last=new Date(Date.UTC(year,month+1,0,12));
   for(let n=0;n<first.getUTCDay();n++){const blank=document.createElement('div');blank.setAttribute('aria-hidden','true');grid.append(blank);}
   for(let n=1;n<=last.getUTCDate();n++){
     const date=new Date(Date.UTC(year,month,n,12)),i=dates.findIndex(d=>key(d)===key(date));
     const cell=document.createElement(i>=0?'button':'div');cell.className='month-cell'+(i<0?' off':'');
     const num=document.createElement('b');num.textContent=format(date,{day:'numeric'});cell.append(num);
     const title=document.createElement('small');title.textContent=i>=0?`${data.modules[Math.floor(i/5)].title} · ${L[data.phases[i%5]]}`:L.off;cell.append(title);
     if(i>=0){cell.type='button';cell.dataset.index=i;if(i===index)cell.classList.add('current');if(key(date)===todayKey())cell.classList.add('is-today');cell.setAttribute('aria-label',`${format(date,{month:'long',day:'numeric'})}. ${title.textContent}`);cell.addEventListener('click',()=>{$('monthDialog').close();go(i);$('monthBtn').focus();});}
     grid.append(cell);
   }
   $('prevMonth').disabled=year<=dates[0].getUTCFullYear()&&month<=dates[0].getUTCMonth();
   const end=dates.at(-1);$('nextMonth').disabled=year>=end.getUTCFullYear()&&month>=end.getUTCMonth();
 }
 function openMonth(){monthDate=new Date(Date.UTC(dates[index].getUTCFullYear(),dates[index].getUTCMonth(),1,12));drawMonth();$('monthDialog').showModal();$('monthDialog').querySelector('[data-close]').focus();}
 async function setProject(on){
   projecting=on;document.body.classList.toggle('projector',on);$('projectBtn').setAttribute('aria-pressed',String(on));
   if(on){$('checkDetails').open=false;$('teacherDetails').open=false;try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();}catch{/* The CSS projector view works when fullscreen is unavailable. */}$('exitProjectBtn').focus();}
   else{if(document.fullscreenElement){try{await document.exitFullscreen();}catch{}}$('projectBtn').focus();}
 }
 buildDates();const startIndex=hashIndex();if(startIndex===null)showToday();else{index=startIndex;render();}
 $('prevBtn').addEventListener('click',()=>go(index-1));$('nextBtn').addEventListener('click',()=>go(index+1));$('todayBtn').addEventListener('click',showToday);
 $('gradeSelect').addEventListener('change',()=>{band=$('gradeSelect').value;save('hlc-grade',band);render();});
 $('monthBtn').addEventListener('click',openMonth);
 $('prevMonth').addEventListener('click',()=>{monthDate.setUTCMonth(monthDate.getUTCMonth()-1);drawMonth();});
 $('nextMonth').addEventListener('click',()=>{monthDate.setUTCMonth(monthDate.getUTCMonth()+1);drawMonth();});
 $('dayJump').addEventListener('change',()=>{const n=Number($('dayJump').value);if(Number.isInteger(n)&&n>=1&&n<=count)go(n-1);else $('dayJump').value=index+1;});
 $('printBtn').addEventListener('click',()=>window.print());
 $('printMonthBtn').addEventListener('click',()=>{document.body.classList.add('print-month');window.print();});
 window.addEventListener('afterprint',()=>document.body.classList.remove('print-month'));
 $('projectBtn').addEventListener('click',()=>setProject(!projecting));$('exitProjectBtn').addEventListener('click',()=>setProject(false));
 document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement&&projecting){projecting=false;document.body.classList.remove('projector');$('projectBtn').setAttribute('aria-pressed','false');$('projectBtn').focus();}});
 $('settingsBtn').addEventListener('click',()=>{$('startDate').value=config.start;$('excludedDates').value=config.excluded.join('\n');$('settingsError').hidden=true;$('settingsDialog').showModal();$('startDate').focus();});
 $('settingsForm').addEventListener('submit',e=>{e.preventDefault();const start=$('startDate').value,excluded=$('excludedDates').value.split(/\s+/).filter(Boolean);if(!valid(start)||excluded.length>1000||excluded.some(x=>!valid(x))){$('settingsError').hidden=false;return;}config={start,excluded:[...new Set(excluded)]};save('hlc-calendar',config);buildDates();$('settingsDialog').close();render();$('settingsBtn').focus();});
 $('resetCalendar').addEventListener('click',()=>{config={start:defaults.start,excluded:[]};save('hlc-calendar',config);buildDates();$('settingsDialog').close();showToday();$('settingsBtn').focus();});
 document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',()=>$(b.dataset.close).close()));
 ['monthDialog','settingsDialog'].forEach(id=>{const dialog=$(id);dialog.addEventListener('click',e=>{const r=dialog.getBoundingClientRect();if(e.target===dialog&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))dialog.close();});});
 $('timerBtn').addEventListener('click',()=>{
   if(timerId){clearInterval(timerId);timerId=null;$('timerBtn').textContent=L.timerStart;$('timerBtn').setAttribute('aria-pressed','false');return;}
   if(timerLeft===0)timerLeft=300;$('timerBtn').textContent=L.timerPause;$('timerBtn').setAttribute('aria-pressed','true');
   timerId=setInterval(()=>{timerLeft--;$('timer').textContent=`${Math.floor(timerLeft/60)}:${String(timerLeft%60).padStart(2,'0')}`;if(timerLeft<=0){clearInterval(timerId);timerId=null;$('timerBtn').textContent=L.timerStart;$('timerBtn').setAttribute('aria-pressed','false');$('live').textContent=L.timerDone;}},1000);
 });
 $('copyBtn').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);$('live').textContent=L.copied;$('copyBtn').textContent=L.copied;setTimeout(()=>$('copyBtn').textContent=L.copyLink,1800);}catch{$('live').textContent=L.copyFailed;}});
 window.addEventListener('hashchange',()=>{const n=hashIndex();if(n!==null){index=n;render('',false);}});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&projecting){setProject(false);return;}if(document.querySelector('dialog[open]')||e.target.closest('input,select,textarea,button,a,summary'))return;const controls={ArrowLeft:()=>go(index-1),PageUp:()=>go(index-1),ArrowRight:()=>go(index+1),PageDown:()=>go(index+1),Home:()=>go(0),End:()=>go(count-1),t:showToday,T:showToday};if(controls[e.key]){e.preventDefault();controls[e.key]();}});
 let swipe=null;page.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'||e.target.closest('a,button,input,select,textarea,summary,details'))return;swipe={x:e.clientX,y:e.clientY};});
 page.addEventListener('pointerup',e=>{if(!swipe)return;const dx=e.clientX-swipe.x,dy=e.clientY-swipe.y;swipe=null;if(Math.abs(dx)>70&&Math.abs(dx)>Math.abs(dy)*1.5)go(index+(dx<0?1:-1));});page.addEventListener('pointercancel',()=>swipe=null);
})();
