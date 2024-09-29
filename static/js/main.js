
let headerRef = document.querySelector("#navbar");
const handleScroll = () => {
    if(headerRef && !headerRef.classList.contains('fit')){
        headerRef.classList.toggle("stick", window.scrollY > 50);
    }
};

window.addEventListener("scroll", handleScroll);


const menuBtn = document.getElementById('menu-button');

menuBtn?.addEventListener('click', e => {
    headerRef?.classList.toggle('active');
})

window.addEventListener('click', e => {
    const target = e.target;
    if ( target.id !== 'menu-button') headerRef?.classList.remove('active');
})