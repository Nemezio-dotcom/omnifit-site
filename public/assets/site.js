/* OmniFit Performance - shared site script (source: site/site.js).
   The footer year script from pages/footer.html is appended by build.py. */
(function(){
  var toggle=document.querySelector('.site-nav-toggle');
  var nav=document.getElementById('site-nav');
  if(!toggle||!nav) return;
  toggle.addEventListener('click',function(){
    var open=nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded',open?'true':'false');
    toggle.setAttribute('aria-label',open?'Close menu':'Open menu');
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&nav.classList.contains('is-open')){
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded','false');
      toggle.setAttribute('aria-label','Open menu');
    }
  });
})();

/* ===== Footer year (source: pages/footer.html) ===== */
(function(){
    var y=document.getElementById('omnifit-year');
    if(y){ y.textContent=new Date().getFullYear(); }
  })();
