//var today = new Date();
//document.getElementById("startDate").value = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
//document.getElementById("stopDate").value = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
BulmaTagsInput.attach();
$('.tabs').each(function(index) {
    var $tabParent = $(this);
    var $tabs = $tabParent.find('li');
    var $contents = $tabParent.next('.tabs-content').find('.tab-content');

    $tabs.click(function() {
      var curIndex = $(this).index();
      // toggle tabs
      $tabs.removeClass('is-active');
      $tabs.eq(curIndex).addClass('is-active');
      // toggle contents
      $contents.removeClass('is-active');
      $contents.eq(curIndex).addClass('is-active');
    });
  });

bulmaToast.setDefaults({
    duration: 5000,
    position: 'bottom-right',
    closeOnClick: true,
    animate: { in: 'fadeIn', out: 'fadeOut' },
    pauseOnHover: true,
    dismissible: true
  })

eel.expose(showalert_nulltext);
function showalert_nulltext(){
    //alertify.error('!!! ไม่ได้ใส่คำค้นหา ใจเย็นๆเด้อ');
    bulmaToast.toast({ type: 'is-danger',message: '!!! ไม่ได้ใส่คำค้นหา ใจเย็นๆเด้อ' });
}

eel.expose(showalert_nulldata);
function showalert_nulldata(){
    //alertify.error('ไม่ข้อมูลในฐานข้อมูลจ้า !');
    bulmaToast.toast({ type: 'is-danger',message: 'ไม่ข้อมูลในฐานข้อมูลจ้า !' });
}

eel.expose(showalert_successdata);
function showalert_successdata(){
    //alertify.success('แสดงข้อมูลเสร็จสิ้น');
    bulmaToast.toast({ type: 'is-success',message: 'แสดงข้อมูลเสร็จสิ้น !' });
}

eel.expose(showalert_successcrawler);
function showalert_successcrawler(){
    //alertify.success('แสดงข้อมูลเสร็จสิ้น');
    bulmaToast.toast({ type: 'is-success',message: 'เก็บข้อมูล Tweets เสร็จสิ้น !' });
}

eel.expose(showalert_searchdata);
function showalert_searchdata(){
    //alertify.message('กำลังค้นหาข้อมูล tweet !');
    bulmaToast.toast({ type: 'is-info',message: 'กำลังค้นหาข้อมูล tweet !' });
}

eel.expose(set_progress_text);
function set_progress_text(text)
{
    //Searching - #lisa
    document.getElementById("progress_text").innerHTML = text;
}

eel.expose(set_progress);
function set_progress(max,val)
{
    var percent_max = max;
    var percent_val = val;
    document.querySelector('progress[id="progress"]').setAttribute("max", percent_max);
    document.querySelector('progress[id="progress"]').setAttribute("value", percent_val);
}

function test() {

    // var confrim = 99;
    // await alertify.confirm("This is a confirm dialog.",
    //     function(){
    //         confrim = 1;
    //     },
    //     function(){
    //         confrim = 0;
    //     });
    /*
    let confirmAction = confirm("Are you sure to execute this action?");
    if (confirmAction) {
      alert("Action successfully executed");
    } else {
      alert("Action canceled");
    }
    console.log("ssss")
    */
    //document.querySelector('progress[id="progress"]').setAttribute("value", "10");
    //$('#progress').prop("value","10");
    table_1.pop();
    bulmaToast.toast({ type: 'is-info',message: 'General Kenobi222' });

}

function test_2() {

    alertify.confirm("This is a confirm dialog.",
        function(){
            confrim = 1;
        },
        function(){
            confrim = 0;
        });
    console.log(confrim)
}

function check() {
    document.getElementById("switch_keyword").checked = true;
  }
  
  function uncheck() {
    document.getElementById("switch_keyword").checked = false;
}