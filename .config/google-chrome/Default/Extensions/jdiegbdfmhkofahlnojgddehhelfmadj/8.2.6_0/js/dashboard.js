
/* global uDom */

'use strict';

/******************************************************************************/

(function() {

/******************************************************************************/

var resizeFrame = function() {
    var navRect = document.getElementById('dashboard-nav').getBoundingClientRect();
    var viewRect = document.documentElement.getBoundingClientRect();
    document.getElementById('iframe').style.setProperty('height', (viewRect.height - navRect.height) + 'px');
};

/******************************************************************************/

var loadDashboardPanel = function() {
    var pane = window.location.hash.slice(1);
    if ( pane === '' ) {
        pane = vAPI.localStorage.getItem('dashboardLastVisitedPane') || 'settings.html';
    } else {
        vAPI.localStorage.setItem('dashboardLastVisitedPane', pane);
    }
    var tabButton = uDom('[href="#' + pane + '"]');
    if ( !tabButton || tabButton.hasClass('selected') ) {
        return;
    }
    uDom('.tabButton.selected').toggleClass('selected', false);
    uDom('iframe').attr('src', pane);
    tabButton.toggleClass('selected', true);
};

/******************************************************************************/

var onTabClickHandler = function(e) {
    var url = window.location.href,
        pos = url.indexOf('#');
    if ( pos !== -1 ) {
        url = url.slice(0, pos);
    }
    url += this.hash;
    if ( url !== window.location.href ) {
        window.location.replace(url);
        loadDashboardPanel();
    }
    e.preventDefault();
};

/******************************************************************************/

uDom.onLoad(function() {
    resizeFrame();
    window.addEventListener('resize', resizeFrame);
    uDom('.tabButton').on('click', onTabClickHandler);
    loadDashboardPanel();
});

/******************************************************************************/

})();
