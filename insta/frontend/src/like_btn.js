import lottie from 'lottie-web';
import likeAnimation from './assets/like_btn.json';
import subscribeAnimation from './assets/purple_cat.json';
const csrftoken = document.querySelector('meta[name="csrf-token"]').content;

document.addEventListener('DOMContentLoaded', () => {

  // --- likes ---
  document.querySelectorAll('[id^="like-button-"]').forEach((btn) => {
    const postId = btn.id.split('-')[2];

    const animation = lottie.loadAnimation({
      container: btn,
      renderer: 'svg',
      loop: false,       // one time
      autoplay: false,
      animationData: likeAnimation,
    });

    btn.addEventListener('click', () => {
      animation.stop();
      animation.goToAndStop(0, true);
      animation.play();
      likePost(postId, btn); // existing functions
    });
  });

  // --- subscribe cat ---
  const subscribeBtn = document.getElementById('subscribe-cat-btn');
  if (subscribeBtn) {
    lottie.loadAnimation({
      container: subscribeBtn,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      animationData: subscribeAnimation,
    });
  }

});

export function likePost(postId, button) {
    fetch(`/like_post/${postId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken, // from meta tag
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        const likesCount = button.nextElementSibling;
        likesCount.textContent = data.likes_count;
    });
}