(() => {
  'use strict';
  const language=document.querySelector('#language');
  language?.addEventListener('change',()=>{const option=language.selectedOptions[0];const hash=location.hash;location.href=option.dataset.url+hash;});
  document.querySelectorAll('[data-print]').forEach(b=>b.addEventListener('click',()=>window.print()));
  const grade=document.querySelector('#activityGrade');
  if(grade){let saved='g35';try{saved=JSON.parse(localStorage.getItem('hlc-grade'))||'g35';}catch{}if(!['k2','g35','g68','g912'].includes(saved))saved='g35';grade.value=saved;const setGrade=()=>{document.querySelectorAll('.band-content').forEach(p=>p.hidden=p.dataset.band!==grade.value);try{localStorage.setItem('hlc-grade',JSON.stringify(grade.value));}catch{}};grade.addEventListener('change',setGrade);setGrade();}
  const search=document.querySelector('#search'),topic=document.querySelector('#topic');
  if(search){const cards=[...document.querySelectorAll('[data-search]')];const count=document.querySelector('#resultCount');const filter=()=>{const query=search.value.normalize('NFKC').toLocaleLowerCase().trim();let n=0;cards.forEach(card=>{const show=card.dataset.search.normalize('NFKC').toLocaleLowerCase().includes(query)&&(!topic.value||card.dataset.topic===topic.value);card.hidden=!show;if(show)n++;});count.textContent=String(n);document.querySelector('#noResults').hidden=n>0;};search.addEventListener('input',filter);topic.addEventListener('change',filter);document.querySelector('#clearFilters').addEventListener('click',()=>{search.value='';topic.value='';filter();search.focus();});filter();}
})();
