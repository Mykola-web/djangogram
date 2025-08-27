import lottie from 'lottie-web';

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("subscribe-btn");
  if (!btn) return;

  const username = btn.dataset.username;
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  btn.addEventListener("click", () => {
    fetch(`/profile/${username}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }

      if (data.is_subscribed) {
        btn.textContent = "Subscribed";
        btn.classList.remove("btn-primary");
        btn.classList.add("btn-secondary");
      } else {
        btn.textContent = "Subscribe";
        btn.classList.remove("btn-secondary");
        btn.classList.add("btn-primary");
      }
    })
    .catch(err => console.error(err));
  });
});
