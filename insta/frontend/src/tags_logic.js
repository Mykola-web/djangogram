import $ from 'jquery';
import 'select2';
import 'select2/dist/css/select2.min.css';

document.addEventListener('DOMContentLoaded', () => {
    $('.select2-chips').select2({
        tags: true,
        theme: 'bootstrap-5',
        placeholder: 'Choose or input tags',
        allowClear: true
    });
});