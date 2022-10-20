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


export function getEdgeDetails(edgeId, utg) {
    var selectedEdge = getEdge(edgeId, utg);
    var edgeInfo = "<h2>Transition Details</h2><hr/>\n";
    var fromState = getNode(selectedEdge.from, utg);
    var toState = getNode(selectedEdge.to, utg);
    edgeInfo += "<img class=\"col-md-5\" src=\"" + fromState.image + "\">\n";
    edgeInfo += "<div class=\"col-md-2 text-center\">TO</div>\n";
    edgeInfo += "<img class=\"col-md-5\" src=\"" + toState.image + "\">\n";
    edgeInfo += "<table class=\"table table-striped\">\n";
    edgeInfo += "<tr class=\"active\"><th colspan=\"4\"><h4>Events</h4></th></tr>\n";;

    var i;
    edgeInfo += "<tr><th>id</th><th>type</th><th>view</th><th>event_str</th></tr>\n";
    for (i = 0; i < selectedEdge.events.length; i++) {
        var event = selectedEdge.events[i];
        var eventStr = event.event_str;
        var viewImg = "";
        if (event.view_images != null) {
            var j;
            for (j = 0; j < event.view_images.length; j++) {
                viewImg += "<img class=\"viewImg\" src=\"" + event.view_images[j] + "\">\n";
            }
        }
        edgeInfo += "<tr><td>" + event.event_id + "</td><td>" + event.event_type + "</td><td>" + viewImg + "</td><td>" + event.event_str + "</td></tr>";
    }
    edgeInfo += "</table>\n";
    return edgeInfo;
}


function getEdge(edgeId, utg) {
    var i, numEdges;
    numEdges = utg.edges.length;
    for (i = 0; i < numEdges; i++) {
        if (utg.edges[i].id == edgeId) {
            return utg.edges[i];
        }
    }
    console.log("cannot find edge: " + edgeId);
};


export function searchUTG(searchKeyword, network, utg) {
    // var searchKeyword = document.getElementById("utgSearchBar").value.toUpperCase();

    searchKeyword = searchKeyword.toUpperCase();
    console.log(searchKeyword);

    if (searchKeyword == null || searchKeyword == "") {
        network.unselectAll();
    } else {
        var i, numNodes;
        var nodes = utg.nodes;
        numNodes = nodes.length;
        var selectedNodes = [];
        for (i = 0; i < numNodes; i++) {
            // console.log(nodes[i].content.toUpperCase());
            if (nodes[i].content.toUpperCase().indexOf(searchKeyword) > -1) {
                selectedNodes.push(nodes[i].id);
            }
        }
        // console.log(selectedNodes);
        network.unselectAll();
        // console.log("Selecting: " + selectedNodes)
        network.selectNodes(selectedNodes, false);
    }
}


export function getOwleyeImage(stateId, UIStates, utg) {
    var node = getNode(stateId, utg);
    var structureId = node.structure_str;
    var result = "<hr><h2>Owleye Result</h2><hr/>\n";

    for (var i = 0; i < UIStates.owleye.length; i++) {
        if (UIStates.owleye[i].structure_id == structureId) {
            return result + "<img class=\"col-md-5\" src='" + UIStates.owleye[i].image + "'/>";
        }
    }

    return "<hr><h2 style=\"color: white\">No Owleye Result</h2><hr/>\n";
}


export function getTappableImage(stateId, UIStates, utg) {
    var node = getNode(stateId, utg);
    var structureId = node.structure_str;
    var result = "<hr><h2>Tappability Result</h2><hr/>\n";

    for (var i = 0; i < UIStates.tappable.length; i++) {
        console.log(UIStates.tappable[i].structure_id);
        if (UIStates.tappable[i].structure_id == structureId) {
            return result + "<img class=\"col-md-5\" src='" + UIStates.tappable[i].image + "'/>";
        }
    }

    return "<hr><h2 style=\"color: white\">No Tappability Result</h2><hr/>\n";
}


export function getXbotImage(stateId, UIStates, utg) {
    var node = getNode(stateId, utg);
    var structureId = node.structure_str;
    var result = "<hr><h2>Xbot Result</h2><hr/>\n";

    for (var i = 0; i < UIStates.xbot.length; i++) {
        console.log(UIStates.xbot[i].structure_id);
        if (UIStates.xbot[i].structure_id == structureId) {
            return result + "<img class=\"col-md-5\" src='" + UIStates.xbot[i].image + "'/>";
        }
    }

    return "<hr><h2 style=\"color: white\">No Xbot Result</h2><hr/>\n";
}
