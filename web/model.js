
function openModal($el) {
  $el.classList.add('is-active');
}
  
function closeModal($el) {
  $el.classList.remove('is-active');
}
  
function closeAllModals() {
  (document.querySelectorAll('.modal') || []).forEach(($modal) => {
    closeModal($modal);
  });
}

async function setModal(keyword_input) {
    //var selector = document.getElementById("twiterdatabase");
    //var selectedText = selector.options[selector.selectedIndex].text;
    console.log(keyword_input)
    document.getElementById("keyword-name").innerHTML = keyword_input;
    var element = document.getElementById("datelist");
    while (element.hasChildNodes()) {
        element.removeChild(element.firstChild);
    }
    state_filter = await eel.get_twitterfilterkeyword(keyword_input)();
    console.log(state_filter);
    if(state_filter == 0){
      document.getElementById("switch_keyword").checked = true;
    }
    else
    {
      document.getElementById("switch_keyword").checked = false;
    }
    date_list = await eel.get_twitterdatekeyword(keyword_input)();
    console.log(date_list);
    for(let i = 0; i < date_list.length; i++) {
      var item = document.createElement("div");
      item.setAttribute("id",date_list[i]);
      item.setAttribute("class","list-item");
      var item_content = document.createElement("div");
      item_content.setAttribute("class","list-item-content");
      var item_content_title = document.createElement("div");
      item_content_title.setAttribute("class","list-item-title");
      item_content_title.innerHTML = date_list[i];
      var item_controls = document.createElement("div");
      item_controls.setAttribute("class","list-item-controls");
      var item_controls_button = document.createElement("div");
      item_controls_button.setAttribute("class","buttons is-right");
      var item_controls_button_button = document.createElement("button");
      item_controls_button_button.setAttribute("class","button is-danger");
      item_controls_button_button.setAttribute("onclick","delete_date"+"("+"'"+keyword_input+"'"+","+"'"+date_list[i]+"'"+")");
      var item_controls_button_button_span = document.createElement("span");
      item_controls_button_button_span.setAttribute("class","icon is-small");
      var item_controls_button_button_span_i = document.createElement("i");
      item_controls_button_button_span_i.setAttribute("class","fa-solid fa-trash-can");
      var item_controls_button_field_label = document.createElement("label");
      item_controls_button_field_label.setAttribute("for","switch_keyword");
      item_controls_button_button_span.appendChild(item_controls_button_button_span_i);
      item_controls_button_button.appendChild(item_controls_button_button_span);
      item_controls_button.appendChild(item_controls_button_button);
      item_content.appendChild(item_content_title);
      item_controls.appendChild(item_controls_button);
      item.appendChild(item_content);
      item.appendChild(item_controls);
      element.appendChild(item);
    }
}

async function setModal_website(keyword_input) {
  //var selector = document.getElementById("twiterdatabase");
  //var selectedText = selector.options[selector.selectedIndex].text;
  console.log(keyword_input)
  document.getElementById("keyword-name").innerHTML = keyword_input;
  var element = document.getElementById("datelist");
  while (element.hasChildNodes()) {
      element.removeChild(element.firstChild);
  }
  state_filter = await eel.get_websitefilter(keyword_input)();
  console.log(state_filter);
  if(state_filter == 0){
    document.getElementById("switch_keyword").checked = true;
  }
  else
  {
    document.getElementById("switch_keyword").checked = false;
  }
  /*
  date_list = await eel.get_twitterdatekeyword(keyword_input)();
  console.log(date_list);
  for(let i = 0; i < date_list.length; i++) {
    var item = document.createElement("div");
    item.setAttribute("id",date_list[i]);
    item.setAttribute("class","list-item");
    var item_content = document.createElement("div");
    item_content.setAttribute("class","list-item-content");
    var item_content_title = document.createElement("div");
    item_content_title.setAttribute("class","list-item-title");
    item_content_title.innerHTML = date_list[i];
    var item_controls = document.createElement("div");
    item_controls.setAttribute("class","list-item-controls");
    var item_controls_button = document.createElement("div");
    item_controls_button.setAttribute("class","buttons is-right");
    var item_controls_button_button = document.createElement("button");
    item_controls_button_button.setAttribute("class","button is-danger");
    item_controls_button_button.setAttribute("onclick","delete_date"+"("+"'"+keyword_input+"'"+","+"'"+date_list[i]+"'"+")");
    var item_controls_button_button_span = document.createElement("span");
    item_controls_button_button_span.setAttribute("class","icon is-small");
    var item_controls_button_button_span_i = document.createElement("i");
    item_controls_button_button_span_i.setAttribute("class","fa-solid fa-trash-can");
    var item_controls_button_field_label = document.createElement("label");
    item_controls_button_field_label.setAttribute("for","switch_keyword");
    item_controls_button_button_span.appendChild(item_controls_button_button_span_i);
    item_controls_button_button.appendChild(item_controls_button_button_span);
    item_controls_button.appendChild(item_controls_button_button);
    item_content.appendChild(item_content_title);
    item_controls.appendChild(item_controls_button);
    item.appendChild(item_content);
    item.appendChild(item_controls);
    element.appendChild(item);
  }
  */
}
// Add a click event on various child elements to close the parent modal
(document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
  const $target = $close.closest('.modal');
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

$("#data-item").click(function() {
  alert(this.value); // get id of clicked li
});