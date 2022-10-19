export function getClusterDetails(clusterId, network, utg) {
    var clusterInfo = "<h2>Cluster Details</h2><hr/>\n";
    var nodeIds = network.getNodesInCluster(clusterId);
    for (var i = 0; i < nodeIds.length; i++) {
        var selectedNode = getNode(nodeIds[i], utg);
        clusterInfo += "<div class=\"row\">\n";
        clusterInfo += "<img class=\"col-md-5\" src=\"" + selectedNode.image + "\">";
        clusterInfo += "<div class=\"col-md-7\">" + selectedNode.title + "</div>";
        clusterInfo += "</div><br />";
    }
    return clusterInfo;
}


function getNode(nodeId, utg) {
    var i;
    var numNodes = utg.nodes.length;
    for (i = 0; i < numNodes; i++) {
        if (utg.nodes[i].id == nodeId) {
            return utg.nodes[i];
        }
    }
    console.log("cannot find node: " + nodeId);
}

export function getOverallResult(utg) {
    var overallInfo = "<hr />";
    overallInfo += "<table class=\"table gifdroid-table\">\n";

    overallInfo += "<tr class=\"active gifdroid-tr\"><th colspan=\"2\" class=\"gifdroid-th\"><h4>App information</h4></th></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\">Package</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.app_package + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\">SHA-256</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.app_sha256 + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\">Main activity</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.app_main_activity + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\"># activities</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.app_num_total_activities + "</td></tr>\n";

    overallInfo += "<tr class=\"active gifdroid-tr\"><th colspan=\"2\"><h4>Device information</h4></th></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\" gifdroid-tq>Device serial</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.device_serial + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\">Model number</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.device_model_number + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\">SDK version</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.device_sdk_version + "</td></tr>\n";

    overallInfo += "<tr class=\"active gifdroid-tr\"><th colspan=\"2\"><h4>DroidBot Result</h4></th></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\">Test date</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.test_date + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\">Time spent (s)</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.time_spent + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\"># input events</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.num_input_events + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\"># UTG states</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.num_nodes + "</td></tr>\n";
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\"># UTG edges</th><td class='gifdroid-td' class=\"col-md-4\">" + utg.num_edges + "</td></tr>\n";
    var activity_coverage = 100 * utg.num_reached_activities / utg.app_num_total_activities;
    overallInfo += "<tr><th class=\"col-md-1 gifdroid-th\">Activity_coverage</th><td class='gifdroid-td' class=\"col-md-4 progress\"><div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"" + utg.num_reached_activities + "\" aria-valuemin=\"0\" aria-valuemax=\"" + utg.app_num_total_activities + "\" style=\"width: " + activity_coverage + "%;\">" + utg.num_reached_activities + "/" + utg.app_num_total_activities + "</div></td></tr>\n";

    overallInfo += "</table>";
    return overallInfo;
}


export function getNodeDetails(nodeId, utg) {
    var selectedNode = getNode(nodeId, utg);
    var stateInfo = "<hr><h2>State Details</h2><hr/>\n";
    stateInfo += "<img class=\"col-md-5\" src=\"" + selectedNode.image + "\">";
    stateInfo += selectedNode.title;
    return stateInfo;
}
