//-----Bootstrap styles:
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

//-----custom static:
import './like_btn.js'
import './tags_logic.js';
import './subscribe.js';

//external libs
import lottie from 'lottie-web';

document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', () => {
        const postId = button.dataset.postId;
        likePost(postId, button);
    });
});

console.log("Webpack ready");