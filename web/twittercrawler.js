var table_tweetdata = new Tabulator("#tweetdata-table", {
    height:650, //810 890 830 set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout:"fitColumns", //fit columns to width of table (optional)
    renderHorizontal:"virtual",
    placeholder:"No Data Set",
    columns:[ //Define Table Columns
        {title:"index", field:"index", hozAlign:"center", width:70},
        {title:"Keyword", field:"keyword", hozAlign:"center", width:100},
        {title:"Date", field:"date", hozAlign:"center", sorter:"date", width:120},
        {title:"Text", field:"text" , formatter:"textarea"},
        {title:"Sentiment", field:"sentiment" , hozAlign:"center", width:100},
        {title:"Retweet", field:"retweet" , hozAlign:"center", width:90},
        {title:"Favorite", field:"fav" , hozAlign:"center", width:90}
    ],
});

var table_tweetstat = new Tabulator("#tweetstat-table", {
    height:376, //520 890 830 set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout:"fitColumns", //fit columns to width of table (optional)
    renderHorizontal:"virtual",
    placeholder:"No Stat",
    columns:[ //Define Table Columns
        {title:"Count", field:"count", hozAlign:"center", width:120},
        {title:"Word", field:"word" , hozAlign:"left"}
    ],
});

function startpage_twitter(){
    console.log("Twitter Page !");
    //get_twittertrend();
    get_twitterdatabase();
    get_Date();
    get_table();
}

eel.expose(refresh_twitter);
function refresh_twitter(){
    console.log("Refresh Twitter Page !");
    //get_twittertrend();
    get_twitterdatabase();
}

async function get_Date()
{
    let date = await eel.get_twittercalendardate()();

    console.log(date);

    const dis_date = [];

    for (let i = 0; i < date[1].length; i++) {
        dis_date.push(new Date(date[1][i]));
    }

    $('#selectDate').multiDatesPicker('destroy');
    if(dis_date.length>0){
        $('#selectDate').multiDatesPicker({
            dateFormat: "yy-mm-dd",
            maxDate:0,
            minDate: -date[0],
            addDisabledDates: dis_date
        });
    }
    else{
        $('#selectDate').multiDatesPicker({
            dateFormat: "yy-mm-dd",
            maxDate:0,
            minDate: -date[0]
        });
    }

}

function get_table()
{

}

async function get_twitterdatabase() {
    console.log("Get Twitter Database");

    $('#twiterdatabase option').remove();

    let data_list = await eel.get_twitterdatabase()();
    console.log(data_list);
    var element = document.getElementById("twiter-database");
    for (let i = 0; i < data_list.length; i++) {

        var list_a = document.createElement("div");
        list_a.setAttribute("class", "list-item");
        //list_a.setAttribute("data-target", "modal-database-manager");
        //list_a.setAttribute("option", data_list[i][0]);

        var list_a_content = document.createElement("a");
        list_a_content.setAttribute("class", "list-item-content print-database");
        list_a_content.setAttribute("value", data_list[i][0]);

        var list_a_content_title = document.createElement("div");
        list_a_content_title.setAttribute("class", "list-item-title is-size-6");
        list_a_content_title.innerHTML = data_list[i][0];

        var list_a_content_description = document.createElement("div");
        list_a_content_description.setAttribute("class", "list-item-description is-size-7");
        list_a_content_description.innerHTML = data_list[i][1] + " Day - " + data_list[i][2] + " tweets";

        var list_a_controls = document.createElement("div");
        list_a_controls.setAttribute("class", "list-item-controls");

        var list_a_controls_buttons = document.createElement("div");
        list_a_controls_buttons.setAttribute("class", "buttons is-right");

        //var list_a_controls_buttons_print = document.createElement("button");
        //list_a_controls_buttons_print.setAttribute("class", "button is-info");
        //list_a_controls_buttons_print.setAttribute("value", "data_list[i][0]");
        //list_a_controls_buttons_print.innerHTML = '<span class="icon is-small"><i class="fa-solid fa-eye"></i></span>';

        var list_a_controls_buttons_edit = document.createElement("button");
        list_a_controls_buttons_edit.setAttribute("class", "button is-danger is-small edit-database");
        list_a_controls_buttons_edit.setAttribute("value", data_list[i][0]);
        list_a_controls_buttons_edit.innerHTML = '<span class="icon is-small"><i class="fa-solid fa-pen-to-square"></i></span>';


        list_a_content.appendChild(list_a_content_title);
        list_a_content.appendChild(list_a_content_description);


        //list_a_controls_buttons.appendChild(list_a_controls_buttons_print);
        list_a_controls_buttons.appendChild(list_a_controls_buttons_edit);
        list_a_controls.appendChild(list_a_controls_buttons);



        list_a.appendChild(list_a_content);
        list_a.appendChild(list_a_controls);

        element.appendChild(list_a);

    }

    $(".print-database").click(function() {
        //alert($(this).attr('value')); // get id of clicked li
        eel.twitter_printkeyword($(this).attr('value'));
        //console.log();
    });

    $(".edit-database").click(function() {
        //alert($(this).attr('value')); // get id of clicked li
        const $target = document.getElementById("modal-database-manager");
        setModal(String($(this).attr('value')));
        openModal($target);
    });
}

async function get_twittertrend() {
    console.log("Get Twitter Trend");
    let trend_list = await eel.get_twittertrend()();
    console.log(trend_list);
    for (let i = 0; i < trend_list.length; i++) {
        var para = document.createElement("option");
        para.setAttribute("option", trend_list[i]);
        var node = document.createTextNode(trend_list[i]);
        para.appendChild(node);
        var element = document.getElementById("twitertrend");
        element.appendChild(para);
    }
}

function set_state_keyword()
{
    if(document.getElementById("switch_keyword").checked == true)
    {
        eel.set_twitterfilterkeyword(document.getElementById("keyword-name").textContent,0);
    }
    else
    {
        eel.set_twitterfilterkeyword(document.getElementById("keyword-name").textContent,1);
    }

    get_Date();
}

function delete_keyword()
{
    eel.twitter_deletekeyword(document.getElementById("keyword-name").textContent);
    get_twitterdatabase();
    get_Date();
}

function delete_date(keyword,date){
    console.log(keyword);
    console.log(date);

    const list = document.getElementById("datelist");
    const list_date = document.getElementById(date);

    const index = Array.from(
        list_date.parentElement.children
      ).indexOf(list_date);

    console.log(index);

    if (list.hasChildNodes()) {
        list.removeChild(list.children[index]);
    }

    eel.twitter_deletedate(keyword,date);
}

function sendSearch_tweet() {
    console.log('Search Tweet');

    //Get time
    var dates = $('#selectDate').multiDatesPicker('getDates');

    if(dates.length > 0)
    {
        eel.searchTweet([$("#inputSearch").val(),dates]);
    }
    else
    {
        console.log('NOOOOO Date');
    }
}

function sendCrawler_tweet() {
    console.log('Clawer Tweet');

    //Get time
    var dates = $('#selectDate').multiDatesPicker('getDates');

    if(dates.length > 0)
    {
        eel.crawlerTweet([$("#inputSearch").val(),dates]);
    }
    else
    {
        console.log('NOOOOO Date');
    }
}

eel.expose(print_tweetdata);
function print_tweetdata(data_input) {
    
    console.log('testdata');

    console.log(data_input);

    table_tweetdata.replaceData(data_input[0]);

    document.getElementById("positive-percent").innerHTML = data_input[1][0];
    document.getElementById("negative-percent").innerHTML = data_input[1][1];
    document.getElementById("neutral-percent").innerHTML = data_input[1][2];

    table_tweetstat.replaceData(data_input[2]);
}

function export_tweet_search()
{
    table_tweetdata.download("csv", "search_export.csv",{bom:true});
}

