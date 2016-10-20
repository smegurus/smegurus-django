/*!
 *
 * Angle - Bootstrap Admin App + jQuery
 *
 * Version: 3.5.1
 * Author: @themicon_co
 * Website: http://themicon.co
 * License: https://wrapbootstrap.com/help/licenses
 *
 */


(function(window, document, $, undefined) {

    if (typeof $ === 'undefined') {
        throw new Error('This application\'s JavaScript requires jQuery');
    }

    $(function() {

        // Restore body classes
        // -----------------------------------
        var $body = $('body');
        new StateToggler().restoreState($body);

        // enable settings toggle after restore
        $('#chk-fixed').prop('checked', $body.hasClass('layout-fixed'));
        $('#chk-collapsed').prop('checked', $body.hasClass('aside-collapsed'));
        $('#chk-collapsed-text').prop('checked', $body.hasClass('aside-collapsed-text'));
        $('#chk-boxed').prop('checked', $body.hasClass('layout-boxed'));
        $('#chk-float').prop('checked', $body.hasClass('aside-float'));
        $('#chk-hover').prop('checked', $body.hasClass('aside-hover'));

        // When ready display the offsidebar
        $('.offsidebar.hide').removeClass('hide');

        // Disable warning "Synchronous XMLHttpRequest on the main thread is deprecated.."
        $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
            options.async = true;
        });

    }); // doc ready

})(window, document, window.jQuery);

// Start Bootstrap JS
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    // POPOVER
    // -----------------------------------

    $('[data-toggle="popover"]').popover();

    // TOOLTIP
    // -----------------------------------

    $('[data-toggle="tooltip"]').tooltip({
      container: 'body'
    });

    // DROPDOWN INPUTS
    // -----------------------------------
    $('.dropdown input').on('click focus', function(event){
      event.stopPropagation();
    });

  });

})(window, document, window.jQuery);


/**=========================================================
 * Module: clear-storage.js
 * Removes a key from the browser storage via element click
 =========================================================*/

(function($, window, document){
  'use strict';

  var Selector = '[data-reset-key]';

  $(document).on('click', Selector, function (e) {
      e.preventDefault();
      var key = $(this).data('resetKey');

      if(key) {
        $.localStorage.remove(key);
        // reload the page
        window.location.reload();
      }
      else {
        $.error('No storage key specified for reset.');
      }
  });

}(jQuery, window, document));

// Color picker
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    if(!$.fn.colorpicker) return;

    $('.demo-colorpicker').colorpicker();

    $('#demo_selectors').colorpicker({
      colorSelectors: {
        'default': '#777777',
        'primary': APP_COLORS['primary'],
        'success': APP_COLORS['success'],
        'info':    APP_COLORS['info'],
        'warning': APP_COLORS['warning'],
        'danger':  APP_COLORS['danger']
      }
    });

  });

})(window, document, window.jQuery);

// GLOBAL CONSTANTS
// -----------------------------------


(function(window, document, $, undefined){

  window.APP_COLORS = {
    'primary':                '#5d9cec',
    'success':                '#27c24c',
    'info':                   '#23b7e5',
    'warning':                '#ff902b',
    'danger':                 '#f05050',
    'inverse':                '#131e26',
    'green':                  '#37bc9b',
    'pink':                   '#f532e5',
    'purple':                 '#7266ba',
    'dark':                   '#3a3f51',
    'yellow':                 '#fad732',
    'gray-darker':            '#232735',
    'gray-dark':              '#3a3f51',
    'gray':                   '#dde6e9',
    'gray-light':             '#e4eaec',
    'gray-lighter':           '#edf1f2'
  };

  window.APP_MEDIAQUERY = {
    'desktopLG':             1200,
    'desktop':                992,
    'tablet':                 768,
    'mobile':                 480
  };

})(window, document, window.jQuery);


// MARKDOWN DOCS
// -----------------------------------


(function(window, document, $, undefined){

  $(function(){

    $('.flatdoc').each(function(){

      Flatdoc.run({

        fetcher: Flatdoc.file('documentation/readme.md'),

        // Setup custom element selectors (markup validates)
        root:    '.flatdoc',
        menu:    '.flatdoc-menu',
        title:   '.flatdoc-title',
        content: '.flatdoc-content'

      });

    });


  });

})(window, document, window.jQuery);

// FULLSCREEN
// -----------------------------------

(function(window, document, $, undefined){

  if ( typeof screenfull === 'undefined' ) return;

  $(function(){

    var $doc = $(document);
    var $fsToggler = $('[data-toggle-fullscreen]');

    // Not supported under IE
    var ua = window.navigator.userAgent;
    if( ua.indexOf("MSIE ") > 0 || !!ua.match(/Trident.*rv\:11\./) ) {
      $fsToggler.addClass('hide');
    }

    if ( ! $fsToggler.is(':visible') ) // hidden on mobiles or IE
      return;

    $fsToggler.on('click', function (e) {
        e.preventDefault();

        if (screenfull.enabled) {

          screenfull.toggle();

          // Switch icon indicator
          toggleFSIcon( $fsToggler );

        } else {
          console.log('Fullscreen not enabled');
        }
    });

    if ( screenfull.raw && screenfull.raw.fullscreenchange)
      $doc.on(screenfull.raw.fullscreenchange, function () {
          toggleFSIcon($fsToggler);
      });

    function toggleFSIcon($element) {
      if(screenfull.isFullscreen)
        $element.children('em').removeClass('fa-expand').addClass('fa-compress');
      else
        $element.children('em').removeClass('fa-compress').addClass('fa-expand');
    }

  });

})(window, document, window.jQuery);

/**=========================================================
 * Module: gmap.js
 * Init Google Map plugin
 =========================================================*/

(function($, window, document){
  'use strict';

  // -------------------------
  // Map Style definition
  // -------------------------

  // Custom core styles
  // Get more styles from http://snazzymaps.com/style/29/light-monochrome
  // - Just replace and assign to 'MapStyles' the new style array
  var MapStyles = [{featureType:'water',stylers:[{visibility:'on'},{color:'#bdd1f9'}]},{featureType:'all',elementType:'labels.text.fill',stylers:[{color:'#334165'}]},{featureType:'landscape',stylers:[{color:'#e9ebf1'}]},{featureType:'road.highway',elementType:'geometry',stylers:[{color:'#c5c6c6'}]},{featureType:'road.arterial',elementType:'geometry',stylers:[{color:'#fff'}]},{featureType:'road.local',elementType:'geometry',stylers:[{color:'#fff'}]},{featureType:'transit',elementType:'geometry',stylers:[{color:'#d8dbe0'}]},{featureType:'poi',elementType:'geometry',stylers:[{color:'#cfd5e0'}]},{featureType:'administrative',stylers:[{visibility:'on'},{lightness:33}]},{featureType:'poi.park',elementType:'labels',stylers:[{visibility:'on'},{lightness:20}]},{featureType:'road',stylers:[{color:'#d8dbe0',lightness:20}]}];


  // -------------------------
  // Custom Script
  // -------------------------

  var mapSelector = '[data-gmap]';

  if($.fn.gMap) {
      var gMapRefs = [];

      $(mapSelector).each(function(){

          var $this   = $(this),
              addresses = $this.data('address') && $this.data('address').split(';'),
              titles    = $this.data('title') && $this.data('title').split(';'),
              zoom      = $this.data('zoom') || 14,
              maptype   = $this.data('maptype') || 'ROADMAP', // or 'TERRAIN'
              markers   = [];

          if(addresses) {
            for(var a in addresses)  {
                if(typeof addresses[a] == 'string') {
                    markers.push({
                        address:  addresses[a],
                        html:     (titles && titles[a]) || '',
                        popup:    true   /* Always popup */
                      });
                }
            }

            var options = {
                controls: {
                       panControl:         true,
                       zoomControl:        true,
                       mapTypeControl:     true,
                       scaleControl:       true,
                       streetViewControl:  true,
                       overviewMapControl: true
                   },
                scrollwheel: false,
                maptype: maptype,
                markers: markers,
                zoom: zoom
                // More options https://github.com/marioestrada/jQuery-gMap
            };

            var gMap = $this.gMap(options);

            var ref = gMap.data('gMap.reference');
            // save in the map references list
            gMapRefs.push(ref);

            // set the styles
            if($this.data('styled') !== undefined) {

              ref.setOptions({
                styles: MapStyles
              });

            }
          }

      }); //each
  }

}(jQuery, window, document));

/**=========================================================
 * Module: Image Cropper
 =========================================================*/

(function(window, document, $, undefined) {

    $(function() {

        if(! $.fn.cropper ) return;

        var $image = $('.img-container > img'),
            $dataX = $('#dataX'),
            $dataY = $('#dataY'),
            $dataHeight = $('#dataHeight'),
            $dataWidth = $('#dataWidth'),
            $dataRotate = $('#dataRotate'),
            options = {
                // data: {
                //   x: 420,
                //   y: 60,
                //   width: 640,
                //   height: 360
                // },
                // strict: false,
                // responsive: false,
                // checkImageOrigin: false

                // modal: false,
                // guides: false,
                // highlight: false,
                // background: false,

                // autoCrop: false,
                // autoCropArea: 0.5,
                // dragCrop: false,
                // movable: false,
                // rotatable: false,
                // zoomable: false,
                // touchDragZoom: false,
                // mouseWheelZoom: false,
                // cropBoxMovable: false,
                // cropBoxResizable: false,
                // doubleClickToggle: false,

                // minCanvasWidth: 320,
                // minCanvasHeight: 180,
                // minCropBoxWidth: 160,
                // minCropBoxHeight: 90,
                // minContainerWidth: 320,
                // minContainerHeight: 180,

                // build: null,
                // built: null,
                // dragstart: null,
                // dragmove: null,
                // dragend: null,
                // zoomin: null,
                // zoomout: null,

                aspectRatio: 16 / 9,
                preview: '.img-preview',
                crop: function(data) {
                    $dataX.val(Math.round(data.x));
                    $dataY.val(Math.round(data.y));
                    $dataHeight.val(Math.round(data.height));
                    $dataWidth.val(Math.round(data.width));
                    $dataRotate.val(Math.round(data.rotate));
                }
            };

        $image.on({
            'build.cropper': function(e) {
                console.log(e.type);
            },
            'built.cropper': function(e) {
                console.log(e.type);
            },
            'dragstart.cropper': function(e) {
                console.log(e.type, e.dragType);
            },
            'dragmove.cropper': function(e) {
                console.log(e.type, e.dragType);
            },
            'dragend.cropper': function(e) {
                console.log(e.type, e.dragType);
            },
            'zoomin.cropper': function(e) {
                console.log(e.type);
            },
            'zoomout.cropper': function(e) {
                console.log(e.type);
            },
            'change.cropper': function(e) {
                console.log(e.type);
            }
        }).cropper(options);


        // Methods
        $(document.body).on('click', '[data-method]', function() {
            var data = $(this).data(),
                $target,
                result;

            if (!$image.data('cropper')) {
                return;
            }

            if (data.method) {
                data = $.extend({}, data); // Clone a new one

                if (typeof data.target !== 'undefined') {
                    $target = $(data.target);

                    if (typeof data.option === 'undefined') {
                        try {
                            data.option = JSON.parse($target.val());
                        } catch (e) {
                            console.log(e.message);
                        }
                    }
                }

                result = $image.cropper(data.method, data.option);

                if (data.method === 'getCroppedCanvas') {
                    $('#getCroppedCanvasModal').modal().find('.modal-body').html(result);
                }

                if ($.isPlainObject(result) && $target) {
                    try {
                        $target.val(JSON.stringify(result));
                    } catch (e) {
                        console.log(e.message);
                    }
                }

            }
        }).on('keydown', function(e) {

            if (!$image.data('cropper')) {
                return;
            }

            switch (e.which) {
                case 37:
                    e.preventDefault();
                    $image.cropper('move', -1, 0);
                    break;

                case 38:
                    e.preventDefault();
                    $image.cropper('move', 0, -1);
                    break;

                case 39:
                    e.preventDefault();
                    $image.cropper('move', 1, 0);
                    break;

                case 40:
                    e.preventDefault();
                    $image.cropper('move', 0, 1);
                    break;
            }

        });


        // Import image
        var $inputImage = $('#inputImage'),
            URL = window.URL || window.webkitURL,
            blobURL;

        if (URL) {
            $inputImage.change(function() {
                var files = this.files,
                    file;

                if (!$image.data('cropper')) {
                    return;
                }

                if (files && files.length) {
                    file = files[0];

                    if (/^image\/\w+$/.test(file.type)) {
                        blobURL = URL.createObjectURL(file);
                        $image.one('built.cropper', function() {
                            URL.revokeObjectURL(blobURL); // Revoke when load complete
                        }).cropper('reset').cropper('replace', blobURL);
                        $inputImage.val('');
                    } else {
                        alert('Please choose an image file.');
                    }
                }
            });
        } else {
            $inputImage.parent().remove();
        }


        // Options
        $('.docs-options :checkbox').on('change', function() {
            var $this = $(this);

            if (!$image.data('cropper')) {
                return;
            }

            options[$this.val()] = $this.prop('checked');
            $image.cropper('destroy').cropper(options);
        });


        // Tooltips
        $('[data-toggle="tooltip"]').tooltip();

    });

})(window, document, window.jQuery);
// LOAD CUSTOM CSS
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    $('[data-load-css]').on('click', function (e) {

      var element = $(this);

      if(element.is('a'))
        e.preventDefault();

      var uri = element.data('loadCss'),
          link;

      if(uri) {
        link = createLink(uri);
        if ( !link ) {
          $.error('Error creating stylesheet link element.');
        }
      }
      else {
        $.error('No stylesheet location defined.');
      }

    });
  });

  function createLink(uri) {
    var linkId = 'autoloaded-stylesheet',
        oldLink = $('#'+linkId).attr('id', linkId + '-old');

    $('head').append($('<link/>').attr({
      'id':   linkId,
      'rel':  'stylesheet',
      'href': uri
    }));

    if( oldLink.length ) {
      oldLink.remove();
    }

    return $('#'+linkId);
  }


})(window, document, window.jQuery);

// TRANSLATION
// -----------------------------------

(function(window, document, $, undefined){

  var preferredLang = 'en';
  var pathPrefix    = 'i18n'; // folder of json files
  var packName      = 'site';
  var storageKey    = 'jq-appLang';

  $(function(){

    if ( ! $.fn.localize ) return;

    // detect saved language or use default
    var currLang = $.localStorage.get(storageKey) || preferredLang;
    // set initial options
    var opts = {
        language: currLang,
        pathPrefix: pathPrefix,
        callback: function(data, defaultCallback){
          $.localStorage.set(storageKey, currLang); // save the language
          defaultCallback(data);
        }
      };

    // Set initial language
    setLanguage(opts);

    // Listen for changes
    $('[data-set-lang]').on('click', function(){

      currLang = $(this).data('setLang');

      if ( currLang ) {

        opts.language = currLang;

        setLanguage(opts);

        activateDropdown($(this));
      }

    });


    function setLanguage(options) {
      $("[data-localize]").localize(packName, options);
    }

    // Set the current clicked text as the active dropdown text
    function activateDropdown(elem) {
      var menu = elem.parents('.dropdown-menu');
      if ( menu.length ) {
        var toggle = menu.prev('button, a');
        toggle.text ( elem.text() );
      }
    }

  });

})(window, document, window.jQuery);

// JVECTOR MAP
// -----------------------------------

(function(window, document, $, undefined){

  window.defaultColors = {
      markerColor:  '#23b7e5',      // the marker points
      bgColor:      'transparent',      // the background
      scaleColors:  ['#878c9a'],    // the color of the region in the serie
      regionFill:   '#bbbec6'       // the base region color
  };

  window.VectorMap = function(element, seriesData, markersData) {

    if ( ! element || !element.length) return;

    var attrs       = element.data(),
        mapHeight   = attrs.height || '300',
        options     = {
          markerColor:  attrs.markerColor  || defaultColors.markerColor,
          bgColor:      attrs.bgColor      || defaultColors.bgColor,
          scale:        attrs.scale        || 1,
          scaleColors:  attrs.scaleColors  || defaultColors.scaleColors,
          regionFill:   attrs.regionFill   || defaultColors.regionFill,
          mapName:      attrs.mapName      || 'world_mill_en'
        };

    element.css('height', mapHeight);

    init( element , options, seriesData, markersData);

    function init($element, opts, series, markers) {

        $element.vectorMap({
          map:             opts.mapName,
          backgroundColor: opts.bgColor,
          zoomMin:         1,
          zoomMax:         8,
          zoomOnScroll:    false,
          regionStyle: {
            initial: {
              'fill':           opts.regionFill,
              'fill-opacity':   1,
              'stroke':         'none',
              'stroke-width':   1.5,
              'stroke-opacity': 1
            },
            hover: {
              'fill-opacity': 0.8
            },
            selected: {
              fill: 'blue'
            },
            selectedHover: {
            }
          },
          focusOn:{ x:0.4, y:0.6, scale: opts.scale},
          markerStyle: {
            initial: {
              fill: opts.markerColor,
              stroke: opts.markerColor
            }
          },
          onRegionLabelShow: function(e, el, code) {
            if ( series && series[code] )
              el.html(el.html() + ': ' + series[code] + ' visitors');
          },
          markers: markers,
          series: {
              regions: [{
                  values: series,
                  scale: opts.scaleColors,
                  normalizeFunction: 'polynomial'
              }]
          },
        });

      }// end init
  };

})(window, document, window.jQuery);

// Morris
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    if ( typeof Morris === 'undefined' ) return;

    var chartdata = [
        { y: "2006", a: 100, b: 90 },
        { y: "2007", a: 75,  b: 65 },
        { y: "2008", a: 50,  b: 40 },
        { y: "2009", a: 75,  b: 65 },
        { y: "2010", a: 50,  b: 40 },
        { y: "2011", a: 75,  b: 65 },
        { y: "2012", a: 100, b: 90 }
    ];

    var donutdata = [
      {label: "Download Sales", value: 12},
      {label: "In-Store Sales",value: 30},
      {label: "Mail-Order Sales", value: 20}
    ];

    // Line Chart
    // -----------------------------------

    new Morris.Line({
      element: 'morris-line',
      data: chartdata,
      xkey: 'y',
      ykeys: ["a", "b"],
      labels: ["Serie A", "Serie B"],
      lineColors: ["#31C0BE", "#7a92a3"],
      resize: true
    });

    // Donut Chart
    // -----------------------------------
    new Morris.Donut({
      element: 'morris-donut',
      data: donutdata,
      colors: [ '#f05050', '#fad732', '#ff902b' ],
      resize: true
    });

    // Bar Chart
    // -----------------------------------
    new Morris.Bar({
      element: 'morris-bar',
      data: chartdata,
      xkey: 'y',
      ykeys: ["a", "b"],
      labels: ["Series A", "Series B"],
      xLabelMargin: 2,
      barColors: [ '#23b7e5', '#f05050' ],
      resize: true
    });

    // Area Chart
    // -----------------------------------
    new Morris.Area({
      element: 'morris-area',
      data: chartdata,
      xkey: 'y',
      ykeys: ["a", "b"],
      labels: ["Serie A", "Serie B"],
      lineColors: [ '#7266ba', '#23b7e5' ],
      resize: true
    });

  });

})(window, document, window.jQuery);

// NAVBAR SEARCH
// -----------------------------------


(function(window, document, $, undefined){

  $(function(){

    var navSearch = new navbarSearchInput();

    // Open search input
    var $searchOpen = $('[data-search-open]');

    $searchOpen
      .on('click', function (e) { e.stopPropagation(); })
      .on('click', navSearch.toggle);

    // Close search input
    var $searchDismiss = $('[data-search-dismiss]');
    var inputSelector = '.navbar-form input[type="text"]';

    $(inputSelector)
      .on('click', function (e) { e.stopPropagation(); })
      .on('keyup', function(e) {
        if (e.keyCode == 27) // ESC
          navSearch.dismiss();
      });

    // click anywhere closes the search
    $(document).on('click', navSearch.dismiss);
    // dismissable options
    $searchDismiss
      .on('click', function (e) { e.stopPropagation(); })
      .on('click', navSearch.dismiss);

  });

  var navbarSearchInput = function() {
    var navbarFormSelector = 'form.navbar-form';
    return {
      toggle: function() {

        var navbarForm = $(navbarFormSelector);

        navbarForm.toggleClass('open');

        var isOpen = navbarForm.hasClass('open');

        navbarForm.find('input')[isOpen ? 'focus' : 'blur']();

      },

      dismiss: function() {
        $(navbarFormSelector)
          .removeClass('open')      // Close control
          .find('input[type="text"]').blur() // remove focus
          // .val('')                    // Empty input
          ;
      }
    };

  }

})(window, document, window.jQuery);
/**=========================================================
 * Module: notify.js
 * Create toggleable notifications that fade out automatically.
 * Based on Notify addon from UIKit (http://getuikit.com/docs/addons_notify.html)
 * [data-toggle="notify"]
 * [data-options="options in json format" ]
 =========================================================*/

(function($, window, document){
  'use strict';

  var Selector = '[data-notify]',
      autoloadSelector = '[data-onload]',
      doc = $(document);


  $(function() {

    $(Selector).each(function(){

      var $this  = $(this),
          onload = $this.data('onload');

      if(onload !== undefined) {
        setTimeout(function(){
          notifyNow($this);
        }, 800);
      }

      $this.on('click', function (e) {
        e.preventDefault();
        notifyNow($this);
      });

    });

  });

  function notifyNow($element) {
      var message = $element.data('message'),
          options = $element.data('options');

      if(!message)
        $.error('Notify: No message specified');

      $.notify(message, options || {});
  }


}(jQuery, window, document));


/**
 * Notify Addon definition as jQuery plugin
 * Adapted version to work with Bootstrap classes
 * More information http://getuikit.com/docs/addons_notify.html
 */

(function($, window, document){

    var containers = {},
        messages   = {},

        notify     =  function(options){

            if ($.type(options) == 'string') {
                options = { message: options };
            }

            if (arguments[1]) {
                options = $.extend(options, $.type(arguments[1]) == 'string' ? {status:arguments[1]} : arguments[1]);
            }

            return (new Message(options)).show();
        },
        closeAll  = function(group, instantly){
            if(group) {
                for(var id in messages) { if(group===messages[id].group) messages[id].close(instantly); }
            } else {
                for(var id in messages) { messages[id].close(instantly); }
            }
        };

    var Message = function(options){

        var $this = this;

        this.options = $.extend({}, Message.defaults, options);

        this.uuid    = "ID"+(new Date().getTime())+"RAND"+(Math.ceil(Math.random() * 100000));
        this.element = $([
            // alert-dismissable enables bs close icon
            '<div class="uk-notify-message alert-dismissable">',
                '<a class="close">&times;</a>',
                '<div>'+this.options.message+'</div>',
            '</div>'

        ].join('')).data("notifyMessage", this);

        // status
        if (this.options.status) {
            this.element.addClass('alert alert-'+this.options.status);
            this.currentstatus = this.options.status;
        }

        this.group = this.options.group;

        messages[this.uuid] = this;

        if(!containers[this.options.pos]) {
            containers[this.options.pos] = $('<div class="uk-notify uk-notify-'+this.options.pos+'"></div>').appendTo('body').on("click", ".uk-notify-message", function(){
                $(this).data("notifyMessage").close();
            });
        }
    };


    $.extend(Message.prototype, {

        uuid: false,
        element: false,
        timout: false,
        currentstatus: "",
        group: false,

        show: function() {

            if (this.element.is(":visible")) return;

            var $this = this;

            containers[this.options.pos].show().prepend(this.element);

            var marginbottom = parseInt(this.element.css("margin-bottom"), 10);

            this.element.css({"opacity":0, "margin-top": -1*this.element.outerHeight(), "margin-bottom":0}).animate({"opacity":1, "margin-top": 0, "margin-bottom":marginbottom}, function(){

                if ($this.options.timeout) {

                    var closefn = function(){ $this.close(); };

                    $this.timeout = setTimeout(closefn, $this.options.timeout);

                    $this.element.hover(
                        function() { clearTimeout($this.timeout); },
                        function() { $this.timeout = setTimeout(closefn, $this.options.timeout);  }
                    );
                }

            });

            return this;
        },

        close: function(instantly) {

            var $this    = this,
                finalize = function(){
                    $this.element.remove();

                    if(!containers[$this.options.pos].children().length) {
                        containers[$this.options.pos].hide();
                    }

                    delete messages[$this.uuid];
                };

            if(this.timeout) clearTimeout(this.timeout);

            if(instantly) {
                finalize();
            } else {
                this.element.animate({"opacity":0, "margin-top": -1* this.element.outerHeight(), "margin-bottom":0}, function(){
                    finalize();
                });
            }
        },

        content: function(html){

            var container = this.element.find(">div");

            if(!html) {
                return container.html();
            }

            container.html(html);

            return this;
        },

        status: function(status) {

            if(!status) {
                return this.currentstatus;
            }

            this.element.removeClass('alert alert-'+this.currentstatus).addClass('alert alert-'+status);

            this.currentstatus = status;

            return this;
        }
    });

    Message.defaults = {
        message: "",
        status: "normal",
        timeout: 5000,
        group: null,
        pos: 'top-center'
    };


    $["notify"]          = notify;
    $["notify"].message  = Message;
    $["notify"].closeAll = closeAll;

    return notify;

}(jQuery, window, document));

// NOW TIMER
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    $('[data-now]').each(function(){
      var element = $(this),
          format = element.data('format');

      function updateTime() {
        var dt = moment( new Date() ).format(format);
        element.text(dt);
      }

      updateTime();
      setInterval(updateTime, 1000);

    });
  });

})(window, document, window.jQuery);

/**=========================================================
 * Module: panel-tools.js
 * Dismiss panels
 * [data-tool="panel-dismiss"]
 *
 * Requires animo.js
 =========================================================*/
(function($, window, document){
  'use strict';

  var panelSelector = '[data-tool="panel-dismiss"]',
      removeEvent   = 'panel.remove',
      removedEvent  = 'panel.removed';

  $(document).on('click', panelSelector, function () {

    // find the first parent panel
    var parent = $(this).closest('.panel');
    var deferred = new $.Deferred();

    // Trigger the event and finally remove the element
    parent.trigger(removeEvent, [parent, deferred]);
    // needs resolve() to be called
    deferred.done(removeElement);

    function removeElement() {
      if($.support.animation) {
        parent.animo({animation: 'bounceOut'}, destroyPanel);
      }
      else destroyPanel();
    }

    function destroyPanel() {
      var col = parent.parent();

      $.when(parent.trigger(removedEvent, [parent]))
       .done(function(){
          parent.remove();
          // remove the parent if it is a row and is empty and not a sortable (portlet)
          col
            .trigger(removedEvent) // An event to catch when the panel has been removed from DOM
            .filter(function() {
            var el = $(this);
            return (el.is('[class*="col-"]:not(.sortable)') && el.children('*').length === 0);
          }).remove();
       });



    }

  });

}(jQuery, window, document));


/**
 * Collapse panels
 * [data-tool="panel-collapse"]
 *
 * Also uses browser storage to keep track
 * of panels collapsed state
 */
(function($, window, document) {
  'use strict';
  var panelSelector = '[data-tool="panel-collapse"]',
      storageKeyName = 'jq-panelState';

  // Prepare the panel to be collapsable and its events
  $(panelSelector).each(function() {
    // find the first parent panel
    var $this        = $(this),
        parent       = $this.closest('.panel'),
        wrapper      = parent.find('.panel-wrapper'),
        collapseOpts = {toggle: false},
        iconElement  = $this.children('em'),
        panelId      = parent.attr('id');

    // if wrapper not added, add it
    // we need a wrapper to avoid jumping due to the paddings
    if( ! wrapper.length) {
      wrapper =
        parent.children('.panel-heading').nextAll() //find('.panel-body, .panel-footer')
          .wrapAll('<div/>')
          .parent()
          .addClass('panel-wrapper');
      collapseOpts = {};
    }

    // Init collapse and bind events to switch icons
    wrapper
      .collapse(collapseOpts)
      .on('hide.bs.collapse', function() {
        setIconHide( iconElement );
        savePanelState( panelId, 'hide' );
        wrapper.prev('.panel-heading').addClass('panel-heading-collapsed');
      })
      .on('show.bs.collapse', function() {
        setIconShow( iconElement );
        savePanelState( panelId, 'show' );
        wrapper.prev('.panel-heading').removeClass('panel-heading-collapsed');
      });

    // Load the saved state if exists
    var currentState = loadPanelState( panelId );
    if(currentState) {
      setTimeout(function() { wrapper.collapse( currentState ); }, 0);
      savePanelState( panelId, currentState );
    }

  });

  // finally catch clicks to toggle panel collapse
  $(document).on('click', panelSelector, function () {

    var parent = $(this).closest('.panel');
    var wrapper = parent.find('.panel-wrapper');

    wrapper.collapse('toggle');

  });

  /////////////////////////////////////////////
  // Common use functions for panel collapse //
  /////////////////////////////////////////////
  function setIconShow(iconEl) {
    iconEl.removeClass('fa-plus').addClass('fa-minus');
  }

  function setIconHide(iconEl) {
    iconEl.removeClass('fa-minus').addClass('fa-plus');
  }

  function savePanelState(id, state) {
    var data = $.localStorage.get(storageKeyName);
    if(!data) { data = {}; }
    data[id] = state;
    $.localStorage.set(storageKeyName, data);
  }

  function loadPanelState(id) {
    var data = $.localStorage.get(storageKeyName);
    if(data) {
      return data[id] || false;
    }
  }


}(jQuery, window, document));


/**
 * Refresh panels
 * [data-tool="panel-refresh"]
 * [data-spinner="standard"]
 */
(function($, window, document){
  'use strict';
  var panelSelector  = '[data-tool="panel-refresh"]',
      refreshEvent   = 'panel.refresh',
      whirlClass     = 'whirl',
      defaultSpinner = 'standard';

  // method to clear the spinner when done
  function removeSpinner(){
    this.removeClass(whirlClass);
  }

  // catch clicks to toggle panel refresh
  $(document).on('click', panelSelector, function () {
      var $this   = $(this),
          panel   = $this.parents('.panel').eq(0),
          spinner = $this.data('spinner') || defaultSpinner
          ;

      // start showing the spinner
      panel.addClass(whirlClass + ' ' + spinner);

      // attach as public method
      panel.removeSpinner = removeSpinner;

      // Trigger the event and send the panel object
      $this.trigger(refreshEvent, [panel]);

  });


}(jQuery, window, document));

/**=========================================================
 * Module: play-animation.js
 * Provides a simple way to run animation with a trigger
 * Targeted elements must have
 *   [data-animate"]
 *   [data-target="Target element affected by the animation"]
 *   [data-play="Animation name (http://daneden.github.io/animate.css/)"]
 *
 * Requires animo.js
 =========================================================*/

(function($, window, document){
  'use strict';

  var Selector = '[data-animate]';

  $(function() {

    var $scroller = $(window).add('body, .wrapper');

    // Parse animations params and attach trigger to scroll
    $(Selector).each(function() {
      var $this     = $(this),
          offset    = $this.data('offset'),
          delay     = $this.data('delay')     || 100, // milliseconds
          animation = $this.data('play')      || 'bounce';

      if(typeof offset !== 'undefined') {

        // test if the element starts visible
        testAnimation($this);
        // test on scroll
        $scroller.scroll(function(){
          testAnimation($this);
        });

      }

      // Test an element visibilty and trigger the given animation
      function testAnimation(element) {
          if ( !element.hasClass('anim-running') &&
              $.Utils.isInView(element, {topoffset: offset})) {
          element
            .addClass('anim-running');

          setTimeout(function() {
            element
              .addClass('anim-done')
              .animo( { animation: animation, duration: 0.7} );
          }, delay);

        }
      }

    });

    // Run click triggered animations
    $(document).on('click', Selector, function() {

      var $this     = $(this),
          targetSel = $this.data('target'),
          animation = $this.data('play') || 'bounce',
          target    = $(targetSel);

      if(target && target.length) {
        target.animo( { animation: animation } );
      }

    });

  });

}(jQuery, window, document));

/**=========================================================
 * Module: portlet.js
 * Drag and drop any panel to change its position
 * The Selector should could be applied to any object that contains
 * panel, so .col-* element are ideal.
 =========================================================*/

(function($, window, document){
  'use strict';

  // Component is optional
  if(!$.fn.sortable) return;

  var Selector = '[data-toggle="portlet"]',
      storageKeyName = 'jq-portletState';

  $(function(){

    $( Selector ).sortable({
      connectWith:          Selector,
      items:                'div.panel',
      handle:               '.portlet-handler',
      opacity:              0.7,
      placeholder:          'portlet box-placeholder',
      cancel:               '.portlet-cancel',
      forcePlaceholderSize: true,
      iframeFix:            false,
      tolerance:            'pointer',
      helper:               'original',
      revert:               200,
      forceHelperSize:      true,
      update:               savePortletOrder,
      create:               loadPortletOrder
    })
    // optionally disables mouse selection
    //.disableSelection()
    ;

  });

  function savePortletOrder(event, ui) {

    var data = $.localStorage.get(storageKeyName);

    if(!data) { data = {}; }

    data[this.id] = $(this).sortable('toArray');

    if(data) {
      $.localStorage.set(storageKeyName, data);
    }

  }

  function loadPortletOrder() {

    var data = $.localStorage.get(storageKeyName);

    if(data) {

      var porletId = this.id,
          panels   = data[porletId];

      if(panels) {
        var portlet = $('#'+porletId);

        $.each(panels, function(index, value) {
           $('#'+value).appendTo(portlet);
        });
      }

    }

  }

}(jQuery, window, document));


// Rickshaw
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    if ( typeof Rickshaw === 'undefined' ) return;

    var seriesData = [ [], [], [] ];
    var random = new Rickshaw.Fixtures.RandomData(150);

    for (var i = 0; i < 150; i++) {
      random.addData(seriesData);
    }

    var series1 = [
      {
        color: "#c05020",
        data: seriesData[0],
        name: 'New York'
      }, {
        color: "#30c020",
        data: seriesData[1],
        name: 'London'
      }, {
        color: "#6060c0",
        data: seriesData[2],
        name: 'Tokyo'
      }
    ];

    var graph1 = new Rickshaw.Graph( {
        element: document.querySelector("#rickshaw1"),
        series:series1,
        renderer: 'area'
    });

    graph1.render();


    // Graph 2
    // -----------------------------------

    var graph2 = new Rickshaw.Graph( {
      element: document.querySelector("#rickshaw2"),
      renderer: 'area',
      stroke: true,
      series: [ {
        data: [ { x: 0, y: 40 }, { x: 1, y: 49 }, { x: 2, y: 38 }, { x: 3, y: 30 }, { x: 4, y: 32 } ],
        color: '#f05050'
      }, {
        data: [ { x: 0, y: 40 }, { x: 1, y: 49 }, { x: 2, y: 38 }, { x: 3, y: 30 }, { x: 4, y: 32 } ],
        color: '#fad732'
      } ]
    } );

    graph2.render();

    // Graph 3
    // -----------------------------------


    var graph3 = new Rickshaw.Graph({
      element: document.querySelector("#rickshaw3"),
      renderer: 'line',
      series: [{
        data: [ { x: 0, y: 40 }, { x: 1, y: 49 }, { x: 2, y: 38 }, { x: 3, y: 30 }, { x: 4, y: 32 } ],
        color: '#7266ba'
      }, {
        data: [ { x: 0, y: 20 }, { x: 1, y: 24 }, { x: 2, y: 19 }, { x: 3, y: 15 }, { x: 4, y: 16 } ],
        color: '#23b7e5'
      }]
    });
    graph3.render();


    // Graph 4
    // -----------------------------------


    var graph4 = new Rickshaw.Graph( {
      element: document.querySelector("#rickshaw4"),
      renderer: 'bar',
      series: [
        {
          data: [ { x: 0, y: 40 }, { x: 1, y: 49 }, { x: 2, y: 38 }, { x: 3, y: 30 }, { x: 4, y: 32 } ],
          color: '#fad732'
        }, {
          data: [ { x: 0, y: 20 }, { x: 1, y: 24 }, { x: 2, y: 19 }, { x: 3, y: 15 }, { x: 4, y: 16 } ],
          color: '#ff902b'

      } ]
    } );
    graph4.render();


  });

})(window, document, window.jQuery);

// Select2
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    if ( !$.fn.select2 ) return;

    // Select 2

    $('#select2-1').select2({
        theme: 'bootstrap'
    });
    $('#select2-2').select2({
        theme: 'bootstrap'
    });
    $('#select2-3').select2({
        theme: 'bootstrap'
    });
    $('#select2-4').select2({
        placeholder: 'Select a state',
        allowClear: true,
        theme: 'bootstrap'
    });

  });

})(window, document, window.jQuery);


// SIDEBAR
// -----------------------------------


(function(window, document, $, undefined){

  var $win;
  var $html;
  var $body;
  var $sidebar;
  var mq;

  $(function(){

    $win     = $(window);
    $html    = $('html');
    $body    = $('body');
    $sidebar = $('.sidebar');
    mq       = APP_MEDIAQUERY;

    // AUTOCOLLAPSE ITEMS
    // -----------------------------------

    var sidebarCollapse = $sidebar.find('.collapse');
    sidebarCollapse.on('show.bs.collapse', function(event){

      event.stopPropagation();
      if ( $(this).parents('.collapse').length === 0 )
        sidebarCollapse.filter('.in').collapse('hide');

    });

    // SIDEBAR ACTIVE STATE
    // -----------------------------------

    // Find current active item
    var currentItem = $('.sidebar .active').parents('li');

    // hover mode don't try to expand active collapse
    if ( ! useAsideHover() )
      currentItem
        .addClass('active')     // activate the parent
        .children('.collapse')  // find the collapse
        .collapse('show');      // and show it

    // remove this if you use only collapsible sidebar items
    $sidebar.find('li > a + ul').on('show.bs.collapse', function (e) {
      if( useAsideHover() ) e.preventDefault();
    });

    // SIDEBAR COLLAPSED ITEM HANDLER
    // -----------------------------------


    var eventName = isTouch() ? 'click' : 'mouseenter' ;
    var subNav = $();
    $sidebar.on( eventName, '.nav > li', function() {

      if( isSidebarCollapsed() || useAsideHover() ) {

        subNav.trigger('mouseleave');
        subNav = toggleMenuItem( $(this) );

        // Used to detect click and touch events outside the sidebar
        sidebarAddBackdrop();
      }

    });

    var sidebarAnyclickClose = $sidebar.data('sidebarAnyclickClose');

    // Allows to close
    if ( typeof sidebarAnyclickClose !== 'undefined' ) {

      $('.wrapper').on('click.sidebar', function(e){
        // don't check if sidebar not visible
        if( ! $body.hasClass('aside-toggled')) return;

        var $target = $(e.target);
        if( ! $target.parents('.aside').length && // if not child of sidebar
            ! $target.is('#user-block-toggle') && // user block toggle anchor
            ! $target.parent().is('#user-block-toggle') // user block toggle icon
          ) {
                $body.removeClass('aside-toggled');
        }

      });
    }

  });

  function sidebarAddBackdrop() {
    var $backdrop = $('<div/>', { 'class': 'dropdown-backdrop'} );
    $backdrop.insertAfter('.aside').on("click mouseenter", function () {
      removeFloatingNav();
    });
  }

  // Open the collapse sidebar submenu items when on touch devices
  // - desktop only opens on hover
  function toggleTouchItem($element){
    $element
      .siblings('li')
      .removeClass('open')
      .end()
      .toggleClass('open');
  }

  // Handles hover to open items under collapsed menu
  // -----------------------------------
  function toggleMenuItem($listItem) {

    removeFloatingNav();

    var ul = $listItem.children('ul');

    if( !ul.length ) return $();
    if( $listItem.hasClass('open') ) {
      toggleTouchItem($listItem);
      return $();
    }

    var $aside = $('.aside');
    var $asideInner = $('.aside-inner'); // for top offset calculation
    // float aside uses extra padding on aside
    var mar = parseInt( $asideInner.css('padding-top'), 0) + parseInt( $aside.css('padding-top'), 0);

    var subNav = ul.clone().appendTo( $aside );

    toggleTouchItem($listItem);

    var itemTop = ($listItem.position().top + mar) - $sidebar.scrollTop();
    var vwHeight = $win.height();

    subNav
      .addClass('nav-floating')
      .css({
        position: isFixed() ? 'fixed' : 'absolute',
        top:      itemTop,
        bottom:   (subNav.outerHeight(true) + itemTop > vwHeight) ? 0 : 'auto'
      });

    subNav.on('mouseleave', function() {
      toggleTouchItem($listItem);
      subNav.remove();
    });

    return subNav;
  }

  function removeFloatingNav() {
    $('.sidebar-subnav.nav-floating').remove();
    $('.dropdown-backdrop').remove();
    $('.sidebar li.open').removeClass('open');
  }

  function isTouch() {
    return $html.hasClass('touch');
  }
  function isSidebarCollapsed() {
    return $body.hasClass('aside-collapsed') || $body.hasClass('aside-collapsed-text');
  }
  function isSidebarToggled() {
    return $body.hasClass('aside-toggled');
  }
  function isMobile() {
    return $win.width() < mq.tablet;
  }
  function isFixed(){
    return $body.hasClass('layout-fixed');
  }
  function useAsideHover() {
    return $body.hasClass('aside-hover');
  }

})(window, document, window.jQuery);
// SKYCONS
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    $('[data-skycon]').each(function(){
      var element = $(this),
          skycons = new Skycons({'color': (element.data('color') || 'white')});

      element.html('<canvas width="' + element.data('width') + '" height="' + element.data('height') + '"></canvas>');

      skycons.add(element.children()[0], element.data('skycon'));

      skycons.play();
    });

  });

})(window, document, window.jQuery);
// SLIMSCROLL
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    $('[data-scrollable]').each(function(){

      var element = $(this),
          defaultHeight = 250;

      element.slimScroll({
          height: (element.data('height') || defaultHeight)
      });

    });
  });

})(window, document, window.jQuery);

// SPARKLINE
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    $('[data-sparkline]').each(initSparkLine);

    function initSparkLine() {
      var $element = $(this),
          options = $element.data(),
          values  = options.values && options.values.split(',');

      options.type = options.type || 'bar'; // default chart is bar
      options.disableHiddenCheck = true;

      $element.sparkline(values, options);

      if(options.resize) {
        $(window).resize(function(){
          $element.sparkline(values, options);
        });
      }
    }
  });

})(window, document, window.jQuery);

// Sweet Alert
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    $('#swal-demo1').on('click', function(e){
      e.preventDefault();
      swal("Here's a message!")
    });


    $('#swal-demo2').on('click', function(e){
      e.preventDefault();
      swal("Here's a message!", "It's pretty, isn't it?")
    });

    $('#swal-demo3').on('click', function(e){
      e.preventDefault();
      swal("Good job!", "You clicked the button!", "success")
    });

    $('#swal-demo4').on('click', function(e){
      e.preventDefault();
      swal({
        title : "Are you sure?",
        text : "You will not be able to recover this imaginary file!",
        type : "warning",
        showCancelButton : true,
        confirmButtonColor : "#DD6B55",
        confirmButtonText : "Yes, delete it!",
        closeOnConfirm : false
      },
        function () {
        swal("Deleted!", "Your imaginary file has been deleted.", "success");
      });

    });

    $('#swal-demo5').on('click', function(e){
      e.preventDefault();
      swal({
        title : "Are you sure?",
        text : "You will not be able to recover this imaginary file!",
        type : "warning",
        showCancelButton : true,
        confirmButtonColor : "#DD6B55",
        confirmButtonText : "Yes, delete it!",
        cancelButtonText : "No, cancel plx!",
        closeOnConfirm : false,
        closeOnCancel : false
      }, function (isConfirm) {
        if (isConfirm) {
          swal("Deleted!", "Your imaginary file has been deleted.", "success");
        } else {
          swal("Cancelled", "Your imaginary file is safe :)", "error");
        }
      });

    });

  });

})(window, document, window.jQuery);

// Custom jQuery
// -----------------------------------


(function(window, document, $, undefined){

  $(function(){

    $('[data-check-all]').on('change', function() {
      var $this = $(this),
          index= $this.index() + 1,
          checkbox = $this.find('input[type="checkbox"]'),
          table = $this.parents('table');
      // Make sure to affect only the correct checkbox column
      table.find('tbody > tr > td:nth-child('+index+') input[type="checkbox"]')
        .prop('checked', checkbox[0].checked);

    });

  });

})(window, document, window.jQuery);


// TOGGLE STATE
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    var $body = $('body');
        toggle = new StateToggler();

    $('[data-toggle-state]')
      .on('click', function (e) {
        // e.preventDefault();
        e.stopPropagation();
        var element = $(this),
            classname = element.data('toggleState'),
            target = element.data('target'),
            noPersist = (element.attr('data-no-persist') !== undefined);

        // Specify a target selector to toggle classname
        // use body by default
        var $target = target ? $(target) : $body;

        if(classname) {
          if( $target.hasClass(classname) ) {
            $target.removeClass(classname);
            if( ! noPersist)
              toggle.removeState(classname);
          }
          else {
            $target.addClass(classname);
            if( ! noPersist)
              toggle.addState(classname);
          }

        }
        // some elements may need this when toggled class change the content size
        // e.g. sidebar collapsed mode and jqGrid
        $(window).resize();

    });

  });

  // Handle states to/from localstorage
  window.StateToggler = function() {

    var storageKeyName  = 'jq-toggleState';

    // Helper object to check for words in a phrase //
    var WordChecker = {
      hasWord: function (phrase, word) {
        return new RegExp('(^|\\s)' + word + '(\\s|$)').test(phrase);
      },
      addWord: function (phrase, word) {
        if (!this.hasWord(phrase, word)) {
          return (phrase + (phrase ? ' ' : '') + word);
        }
      },
      removeWord: function (phrase, word) {
        if (this.hasWord(phrase, word)) {
          return phrase.replace(new RegExp('(^|\\s)*' + word + '(\\s|$)*', 'g'), '');
        }
      }
    };

    // Return service public methods
    return {
      // Add a state to the browser storage to be restored later
      addState: function(classname){
        var data = $.localStorage.get(storageKeyName);

        if(!data)  {
          data = classname;
        }
        else {
          data = WordChecker.addWord(data, classname);
        }

        $.localStorage.set(storageKeyName, data);
      },

      // Remove a state from the browser storage
      removeState: function(classname){
        var data = $.localStorage.get(storageKeyName);
        // nothing to remove
        if(!data) return;

        data = WordChecker.removeWord(data, classname);

        $.localStorage.set(storageKeyName, data);
      },

      // Load the state string and restore the classlist
      restoreState: function($elem) {
        var data = $.localStorage.get(storageKeyName);

        // nothing to restore
        if(!data) return;
        $elem.addClass(data);
      }

    };
  };

})(window, document, window.jQuery);

// Bootstrap Tour
// -----------------------------------

(function(window, document, $, undefined){

  $(function(){

    // Prepare steps
    var tourSteps = [];
    $('.tour-step').each(function(){
      var stepsOptions = $(this).data();
      stepsOptions.element = '#'+this.id;
      tourSteps.push( stepsOptions );
    });

    if ( tourSteps.length ) {
      // Instance the tour
      var tour = new Tour({
          backdrop: true,
          onShown: function(tour) {
            // BootstrapTour is not compatible with z-index based layout
            // so adding position:static for this case makes the browser
            // to ignore the property
            $('.wrapper > section').css({'position': 'static'});
          },
          onHide: function (tour) {
            // finally restore on destroy and reuse the value declared in stylesheet
            $('.wrapper > section').css({'position': ''});
          },
          steps: tourSteps
        });

      // Initialize the tour
      tour.init();


      $('#start-tour').on('click', function(){
        // Start the tour
        tour.restart();
      });
    }

  });

})(window, document, window.jQuery);

/**=========================================================
 * Module: trigger-resize.js
 * Triggers a window resize event from any element
 =========================================================*/

(function(window, document, $, undefined) {

    $(function() {
        var element = $('[data-trigger-resize]');
        var value = element.data('triggerResize')
        element.on('click', function() {
            setTimeout(function() {
                // all IE friendly dispatchEvent
                var evt = document.createEvent('UIEvents');
                evt.initUIEvent('resize', true, false, window, 0);
                window.dispatchEvent(evt);
                // modern dispatchEvent way
                // window.dispatchEvent(new Event('resize'));
            }, value || 300);
        });
    });

})(window, document, window.jQuery);
/**=========================================================
 * Module: utils.js
 * jQuery Utility functions library
 * adapted from the core of UIKit
 =========================================================*/

(function($, window, doc){
    'use strict';

    var $html = $("html"), $win = $(window);

    $.support.transition = (function() {

        var transitionEnd = (function() {

            var element = doc.body || doc.documentElement,
                transEndEventNames = {
                    WebkitTransition: 'webkitTransitionEnd',
                    MozTransition: 'transitionend',
                    OTransition: 'oTransitionEnd otransitionend',
                    transition: 'transitionend'
                }, name;

            for (name in transEndEventNames) {
                if (element.style[name] !== undefined) return transEndEventNames[name];
            }
        }());

        return transitionEnd && { end: transitionEnd };
    })();

    $.support.animation = (function() {

        var animationEnd = (function() {

            var element = doc.body || doc.documentElement,
                animEndEventNames = {
                    WebkitAnimation: 'webkitAnimationEnd',
                    MozAnimation: 'animationend',
                    OAnimation: 'oAnimationEnd oanimationend',
                    animation: 'animationend'
                }, name;

            for (name in animEndEventNames) {
                if (element.style[name] !== undefined) return animEndEventNames[name];
            }
        }());

        return animationEnd && { end: animationEnd };
    })();

    $.support.requestAnimationFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.msRequestAnimationFrame || window.oRequestAnimationFrame || function(callback){ window.setTimeout(callback, 1000/60); };
    $.support.touch                 = (
        ('ontouchstart' in window && navigator.userAgent.toLowerCase().match(/mobile|tablet/)) ||
        (window.DocumentTouch && document instanceof window.DocumentTouch)  ||
        (window.navigator['msPointerEnabled'] && window.navigator['msMaxTouchPoints'] > 0) || //IE 10
        (window.navigator['pointerEnabled'] && window.navigator['maxTouchPoints'] > 0) || //IE >=11
        false
    );
    $.support.mutationobserver      = (window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver || null);

    $.Utils = {};

    $.Utils.debounce = function(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };

    $.Utils.removeCssRules = function(selectorRegEx) {
        var idx, idxs, stylesheet, _i, _j, _k, _len, _len1, _len2, _ref;

        if(!selectorRegEx) return;

        setTimeout(function(){
            try {
              _ref = document.styleSheets;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                stylesheet = _ref[_i];
                idxs = [];
                stylesheet.cssRules = stylesheet.cssRules;
                for (idx = _j = 0, _len1 = stylesheet.cssRules.length; _j < _len1; idx = ++_j) {
                  if (stylesheet.cssRules[idx].type === CSSRule.STYLE_RULE && selectorRegEx.test(stylesheet.cssRules[idx].selectorText)) {
                    idxs.unshift(idx);
                  }
                }
                for (_k = 0, _len2 = idxs.length; _k < _len2; _k++) {
                  stylesheet.deleteRule(idxs[_k]);
                }
              }
            } catch (_error) {}
        }, 0);
    };

    $.Utils.isInView = function(element, options) {

        var $element = $(element);

        if (!$element.is(':visible')) {
            return false;
        }

        var window_left = $win.scrollLeft(),
            window_top  = $win.scrollTop(),
            offset      = $element.offset(),
            left        = offset.left,
            top         = offset.top;

        options = $.extend({topoffset:0, leftoffset:0}, options);

        if (top + $element.height() >= window_top && top - options.topoffset <= window_top + $win.height() &&
            left + $element.width() >= window_left && left - options.leftoffset <= window_left + $win.width()) {
          return true;
        } else {
          return false;
        }
    };

    $.Utils.options = function(string) {

        if ($.isPlainObject(string)) return string;

        var start = (string ? string.indexOf("{") : -1), options = {};

        if (start != -1) {
            try {
                options = (new Function("", "var json = " + string.substr(start) + "; return JSON.parse(JSON.stringify(json));"))();
            } catch (e) {}
        }

        return options;
    };

    $.Utils.events       = {};
    $.Utils.events.click = $.support.touch ? 'tap' : 'click';

    $.langdirection = $html.attr("dir") == "rtl" ? "right" : "left";

    $(function(){

        // Check for dom modifications
        if(!$.support.mutationobserver) return;

        // Install an observer for custom needs of dom changes
        var observer = new $.support.mutationobserver($.Utils.debounce(function(mutations) {
            $(doc).trigger("domready");
        }, 300));

        // pass in the target node, as well as the observer options
        observer.observe(document.body, { childList: true, subtree: true });

    });

    // add touch identifier class
    $html.addClass($.support.touch ? "touch" : "no-touch");

}(jQuery, window, document));
// Custom jQuery
// -----------------------------------


(function(window, document, $, undefined){

  $(function(){

    // document ready

  });

})(window, document, window.jQuery);
