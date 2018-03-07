 odoo.define('web_debranding_globalteckz.rebranding', function (require) {
"use strict";

var ajax = require('web.ajax');
var WebClient = require('web.WebClient');
var utils = require('web.utils');

WebClient.extend({
	init: function(parent) {
		var self = this;
        this.client_options = {};
        this._super(parent);
        this.origin = undefined;
        this._current_state = null;
        this.menu_dm = new utils.DropMisordered();
        this.action_mutex = new utils.Mutex();
        ajax.jsonRpc('/get_css_selected/', 'call', {}).then(function (brand_vals) {
        	var brand_vals = JSON.parse(brand_vals);
        	if(brand_vals.brand_name){
        		self.set('title_part', {"zopenerp": brand_vals.brand_name});
        	}else{
        		self.set('title_part', {"zopenerp": 'Odoo'});
        	}
    	});
    },
});


$(document).ready(function () {
	$('.oe_view_manager_buttons').click(function(){});
		ajax.jsonRpc('/get_css_selected/', 'call', {}).then(function (css_vals) {
			console.log('cssssssssssssssss'+css_vals)
			css_vals = JSON.parse(css_vals);
			
			//for brand info
			var val = '<a href="http://'+ css_vals.brand_website + '" target="_blank" id="brand_footer">Powered by<span> ' + css_vals.brand_name +'</span></a>';
			$("#brand_footer").html(val);
			/*var href = 'data:image/png;,' + css_vals.favicon
			$("head link[rel='icon']").attr('href',href);*/
			
	//	    //SIDEBAR IMAGE
	//	    $(".oe_submenu").css("background-image", css_vals.sidebar_image);
	//	    //TOP IMAGE
	//	    var topBg_IMG_FORMAT = 'url("data:image/gif;base64,'+ css_vals.top_image +'")'
	//	    $(".navbar-collapse").css("background-image", topBg_IMG_FORMAT);
		    //COLOR
		    //SIDEBAR FONT
		    if(css_vals.leftfont_color){
		    	$(".oe_secondary_menu > ul > li > a").css("color", css_vals.leftfont_color);
		    }
		    
		    //SIDEBAR FONT - PARENT MENU
		    if (css_vals.leftfont_color_parent){
		    	$(".oe_secondary_menu_section").css("color", css_vals.leftfont_color_parent);
		    }
		    
		    //TOP BAR FONT
		    if (css_vals.menu_font_color){
		    	$(".navbar-inverse .navbar-nav > li > a").css("color", css_vals.menu_font_color);
		    }
		    //TOP BAR BACKGROUND COLOR
		    if (css_vals.menu_background_color){
		    	$(".navbar-collapse.collapse").css("background-color", css_vals.menu_background_color);
		    }
		    //SIDE BAR BACKGROUND COLOR
		    if (css_vals.left_background_color){
		    	$(".o_sub_menu").css("background-color", css_vals.left_background_color);
		    }
		    //FONT STYLE
		    //SIDE
		    if (css_vals.font_common){
		    	$(".oe_leftbar").css("font-family", css_vals.font_common);
		    	$("a").css("font-family", css_vals.font_common);
		    }
		
		});
	});
});
