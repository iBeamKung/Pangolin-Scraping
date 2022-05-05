var table_webdata = new Tabulator("#webdata-table", {
    height:650, //810 890 830 set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout:"fitColumns", //fit columns to width of table (optional)
    renderHorizontal:"virtual",
    placeholder:"No WebScraping Data Set",
    columns:[ //Define Table Columns
        {title:"index", field:"index", hozAlign:"center", width:90},
        {title:"Link", field:"link" , formatter:"link" , formatterParams:{ target:"_blank",} },
        {title:"Create at", field:"create_at", hozAlign:"center", width:110},
        {title:"Lang", field:"lang", hozAlign:"center", width:90},
        {title:"Header", field:"header"},
        {title:"Content", field:"content"},
        {title:"Sentiment", field:"sentiment", hozAlign:"center", width:120},
        {title:"Crawler at", field:"crawler_at", hozAlign:"center", width:110},
        {title:"href", field:"href_link"},
    ],
});

var table_webstat_1 = new Tabulator("#webstat-table-1", {
    height:376, //520 890 830 set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout:"fitColumns", //fit columns to width of table (optional)
    renderHorizontal:"virtual",
    placeholder:"No Stat",
    columns:[ //Define Table Columns
        {title:"Count", field:"count", hozAlign:"center", width:120},
        {title:"Word", field:"word" , hozAlign:"left"}
    ],
});

var table_webstat_2 = new Tabulator("#webstat-table-2", {
    height:376, //520 890 830 set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout:"fitColumns", //fit columns to width of table (optional)
    renderHorizontal:"virtual",
    placeholder:"No Stat",
    columns:[ //Define Table Columns
        {title:"Count", field:"count", hozAlign:"center", width:120},
        {title:"Link", field:"link" , hozAlign:"left", formatter:"link" , formatterParams:{ target:"_blank",}}
    ],
});

function startpage_webscraping(){
    console.log("WebScraping Page !");
    get_websitedatabase();
}

function sendSearch_web() {
    console.log('Search Web');
    eel.searchWeb($("#inputCrawler").val());
}

async function get_websitedatabase() {
    console.log("Get Website Database");

    //$('#twiterdatabase option').remove();

    let data_list = await eel.get_websitedatabase()();
    console.log(data_list);
    var element = document.getElementById("website-database");
    for (let i = 0; i < data_list.length; i++) {

        var list_a = document.createElement("div");
        list_a.setAttribute("class", "list-item");
        //list_a.setAttribute("data-target", "modal-database-manager");
        //list_a.setAttribute("option", data_list[i][0]);

        var list_a_content = document.createElement("a");
        list_a_content.setAttribute("class", "list-item-content website-print-database");
        list_a_content.setAttribute("value", data_list[i][0]);

        var list_a_content_title = document.createElement("div");
        list_a_content_title.setAttribute("class", "list-item-title is-size-6");
        list_a_content_title.innerHTML = data_list[i][0];

        var list_a_content_description = document.createElement("div");
        list_a_content_description.setAttribute("class", "list-item-description is-size-7");
        list_a_content_description.innerHTML = "Total Page : " + data_list[i][1];

        var list_a_controls = document.createElement("div");
        list_a_controls.setAttribute("class", "list-item-controls");

        var list_a_controls_buttons = document.createElement("div");
        list_a_controls_buttons.setAttribute("class", "buttons is-right");

        //var list_a_controls_buttons_print = document.createElement("button");
        //list_a_controls_buttons_print.setAttribute("class", "button is-info");
        //list_a_controls_buttons_print.setAttribute("value", "data_list[i][0]");
        //list_a_controls_buttons_print.innerHTML = '<span class="icon is-small"><i class="fa-solid fa-eye"></i></span>';

        var list_a_controls_buttons_edit = document.createElement("button");
        list_a_controls_buttons_edit.setAttribute("class", "button is-danger is-small website-edit-database");
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

    $(".website-print-database").click(function() {
        //alert($(this).attr('value')); // get id of clicked li
        eel.website_printdata($(this).attr('value'));
        //console.log();
    });

    $(".website-edit-database").click(function() {
        //alert($(this).attr('value')); // get id of clicked li
        const $target = document.getElementById("modal-database-manager");
        setModal_website(String($(this).attr('value')));
        openModal($target);
    });
}

function set_state_website()
{
    if(document.getElementById("switch_keyword").checked == true)
    {
        eel.set_websitefilter(document.getElementById("keyword-name").textContent,0);
    }
    else
    {
        eel.set_websitefilter(document.getElementById("keyword-name").textContent,1);
    }
}

function delete_website()
{
    eel.twitter_deletekeyword(document.getElementById("keyword-name").textContent);
    get_twitterdatabase();
}

/*
eel.expose(print_webdata);
function print_webdata(data_input) {
    console.log('print_webdata');
    var table = new Tabulator("#tweetdata-table", {
        height:900, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
        data:data_input, //assign data to table
        layout:"fitColumns", //fit columns to width of table (optional)
        renderHorizontal:"virtual",
        columns:[ //Define Table Columns
            {title:"index", field:"index", hozAlign:"center", width:90},
            {title:"Link", field:"link" , formatter:"link" , formatterParams:{ target:"_blank",} },
            {title:"Create at", field:"create_at", hozAlign:"center", width:110},
            {title:"Lang", field:"lang", hozAlign:"center", width:90},
            {title:"Header", field:"header"},
            {title:"Content", field:"content"},
            {title:"Sentiment", field:"sentiment", hozAlign:"center", width:120},
            {title:"Crawler at", field:"crawler_at", hozAlign:"center", width:110},
            {title:"href", field:"href_link"},
            //{title:"Sentiment", field:"sentiment" , hozAlign:"center", width:100},
        ],
    });
}
*/

eel.expose(print_webdata);
function print_webdata(data_input) {
    
    console.log('Print Webdata');

    console.log(data_input);

    table_webdata.replaceData(data_input[0]);

    document.getElementById("positive-percent").innerHTML = data_input[1][0];
    document.getElementById("negative-percent").innerHTML = data_input[1][1];
    document.getElementById("neutral-percent").innerHTML = data_input[1][2];

    table_webstat_1.replaceData(data_input[2]);
    table_webstat_2.replaceData(data_input[3]);
}

function export_web_search()
{
    table_webdata.download("csv", "search_export.csv",{bom:true});
}

function add_web_abcnews()
{
    eel.add_website("abcnews",document.getElementById("abcnews").value);
}
function add_web_amarin()
{
    eel.add_website("amarin",document.getElementById("amarin").value);
}
function add_web_bangkokpost()
{
    eel.add_website("bangkokpost",document.getElementById("bangkokpost").value);
}
function add_web_bbc()
{
    eel.add_website("bbc",document.getElementById("bbc").value);
}
function add_web_businesstoday()
{
    eel.add_website("businesstoday",document.getElementById("businesstoday").value);
}

function add_web_cbc()
{
    eel.add_website("cbc",document.getElementById("cbc").value);
}
function add_web_cnn()
{
    eel.add_website("cnn",document.getElementById("cnn").value);
}
function aadd_web_cryptosiam()
{
    eel.add_website("cryptosiam",document.getElementById("cryptosiam").value);
}
function add_web_dailymail()
{
    eel.add_website("dailymail",document.getElementById("dailymail").value);
}
function add_web_foxbusiness()
{
    eel.add_website("foxbusiness",document.getElementById("foxbusiness").value);
}

function add_web_kaohoon()
{
    eel.add_website("kaohoon",document.getElementById("kaohoon").value);
}
function add_web_khaosod()
{
    eel.add_website("khaosod",document.getElementById("khaosod").value);
}
function add_web_mrgonline()
{
    eel.add_website("mrgonline",document.getElementById("mrgonline").value);
}
function add_web_nbcnews()
{
    eel.add_website("nbcnews",document.getElementById("nbcnews").value);
}
function add_web_sanook()
{
    eel.add_website("sanook",document.getElementById("sanook").value);
}

function add_web_siambitcoin()
{
    eel.add_website("siambitcoin",document.getElementById("siambitcoin").value);
}
function add_web_tbn()
{
    eel.add_website("tbn",document.getElementById("tbn").value);
}
function add_web_thairath()
{
    eel.add_website("thairath",document.getElementById("thairath").value);
}
function add_web_tnn()
{
    eel.add_website("tnn",document.getElementById("tnn").value);
}
function add_web_trueid()
{
    eel.add_website("trueid",document.getElementById("trueid").value);
}

function Crawler_web()
{
    eel.crawler_web();
}