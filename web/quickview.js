document.addEventListener('DOMContentLoaded', () => {
    // Functions to open and close a modal
    var quickviews = bulmaQuickview.attach();
    function openModal($el) {
      $el.classList.add('is-active');
    }
  
    function closeModal($el) {
      $el.classList.remove('is-active');
    }
  
    function closeAllModals() {
      (document.querySelectorAll('.quickview') || []).forEach(($quickview) => {
        closeModal($quickview);
      });
    }

    async function setModal() {
          console.log("HELLOOOO");
      }
  
    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
      const modal = $trigger.dataset.target;
      const $target = document.getElementById(modal);
      console.log($target);

      $trigger.addEventListener('dblclick', () => {
        setModal();
        openModal($target);
      });
    
    });
  
    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.quickview-header .delete') || []).forEach(($close) => {
      const $target = $close.closest('.quickview');
  
      $close.addEventListener('click', () => {
        closeModal($target);
      });
    });
  
    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
      const e = event || window.event;
  
      if (e.keyCode === 27) { // Escape key
        closeAllModals();
      }
    });
  });