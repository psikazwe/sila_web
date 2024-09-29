class InfiniteCarousel {
    constructor(container) {
      this.container = container;
      this.wrapper = container.querySelector('.wrapper');
      this.slides = [];
      this.currentIndex = 0;
      this.isPlaying = true;
  
      this.setupEventListeners();
      this.addInitialSlides();
  
      // Start autoplay when mounted
      this.startAutoplay();
    }
  
    setupEventListeners() {
      this.wrapper.addEventListener('transitionend', () => {
        this.checkIndex();
        this.updateIndicator();
      });
    }
  
    addInitialSlides() {
      const slides = document.querySelectorAll('.slide');
      this.slides = Array.from(slides).concat(Array.from(slides));
      this.wrapper.innerHTML = '';
      this.slides.forEach((slide, index) => {
        this.wrapper.appendChild(this.slides[index]);
      });
    }
  
    move(direction) {
      const { wrapper } = this;
      const { slides } = this;
      const currentTranslateX = parseFloat(getComputedStyle(wrapper).transform.split(',')[4]);
  
      wrapper.style.transition = 'transform 0.3s ease';
      wrapper.style.transform = `translateX(${currentTranslateX + direction * 100}%)`;
  
      setTimeout(() => {
        wrapper.style.transition = '';
      }, 300);
    }
  
    checkIndex() {
      const { wrapper } = this;
      const { slides } = this;
      const currentIndex = parseInt(getComputedStyle(wrapper).transform.split(',')[4]) / 100;
      
      if (currentIndex <= -1) {
        this.moveToOriginalPosition();
      } else if (currentIndex >= slides.length - 1) {
        this.moveToOriginalPosition();
      }
    }
  
    moveToOriginalPosition() {
      const { wrapper } = this;
      const { slides } = this;
      const originalPosition = Math.floor(slides.length / 2);
  
      wrapper.style.transition = 'transform 0.3s ease';
      wrapper.style.transform = `translateX(${-originalPosition * 100}%)`;
    }
    startAutoplay() {
      this.playing = true;
      this.autoplayInterval = setInterval(() => this.move(1), 5000); // Adjust delay as needed
    }
  
  }
  
  // Usage
  // const autoplayToggle = document.getElementById('autoplay-toggle');
  // const carousel = new InfiniteCarousel(
  //   document.querySelector('.carousel-container'),
  // );
  

  const container = document.querySelector('.marquee-container');
  let speed = 10;

  function updateSpeed() {
      speed += 0.1;
      container.style.animationDuration = `${speed}s`;
  }

  function init() {
      window.addEventListener('scroll', updateSpeed);
      requestAnimationFrame(init);
  }

  init();