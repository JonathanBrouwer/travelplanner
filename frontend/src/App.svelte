<script lang="ts">
    import {CircleMarker, LeafletMap, TileLayer, Polyline} from 'svelte-leafletjs';
    import {onMount} from "svelte";
    import {LatLng, LeafletMouseEvent} from "leaflet";
    import RouteOverview from "./RouteOverview.svelte";
    import {getClosestStation, getRoute, onError, Point} from "./api";
    import {RoutePoint, RoutePointType} from "./data";

    let routepoints: RoutePoint[] = [];
    let points: Point[] = [];

    let mapOptions = {
        center: [0, 0],
        zoom: 3,
    };

    const onMapClick = async (e) => {
        const location = (e as LeafletMouseEvent).latlng;
        const new_length = points.push({
            lat: location.lat,
            lng: location.lng,
        });
        points = points;

        let closest = await getClosestStation({
            lat: location.lat,
            lng: location.lng,
        });

        if (closest !== null) {
            const found = routepoints.find((i) => {
                return i.description == closest.name;
            });
            if (typeof found !== "undefined") {
                onError("duplicate station");
            } else {
                const rp = RoutePoint.randomColour(
                    closest.name,
                    RoutePointType.SingleStation,
                )

                rp.lat = closest.lat;
                rp.lng = closest.lng;

                routepoints = [...routepoints, rp];
            }
        }

        points.splice(new_length - 1, 1);
        points = points;
    }

    onMount(() => {
        navigator.geolocation.getCurrentPosition((pos) => {
            const map = leafletMap.getMap();
            console.log(`moving to ${pos.coords.latitude}; ${pos.coords.longitude}`);
            map.setZoom(10);
            map.setView(new LatLng(pos.coords.latitude, pos.coords.longitude));
        }, (err) => {
            console.error(err.message)
        })

        leafletMap.getMap().on("click", onMapClick)
    })

    // const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    const tileUrl = "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
    // const tileUrl = "https://maps.geoapify.com/v1/tile/osm-bright-smooth/{z}/{x}/{y}.png"

    const railUrl = "https://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png "

    const tileLayerOptions = {
        minZoom: 0,
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution: "© OpenStreetMap contributors",
    };

    const split = (index) => {
        const route = routepoints[index];
        if (route.type == RoutePointType.SingleStation) {
            return;
        }

        routepoints[index] = route.fromobj;
        routepoints.splice(index + 1, 0, route.toobj);
        routepoints = routepoints;
    }

    const focus = (lat, lng, zoom) => {
        const map = leafletMap.getMap();

        let pzoom = typeof zoom !== "undefined" ? zoom : 8;
        map.setView(new LatLng(lat, lng), pzoom);
    }

    const remove = (index) => {
        routepoints.splice(index, 1);
        routepoints = routepoints;
    }

    const merge = (indexa, indexb) => {
        const olda = routepoints[indexa];
        const oldb = routepoints[indexb];

        const astart = olda.type === RoutePointType.SingleStation ? olda.description : olda.from;
        const bend = oldb.type === RoutePointType.SingleStation ? oldb.description : oldb.to;

        let r = new RoutePoint(
            "",
            olda.colour,
            RoutePointType.Route,
        )

        r.from = astart;
        r.to = bend;
        r.fromobj = olda;
        r.toobj = oldb;

        routepoints[indexa] = r;

        getRoute(
            r.getLatFrom(),
            r.getLngFrom(),
            r.getLatTo(),
            r.getLngTo(),
        ).then((res) => {
            r.segments = res;
            console.log(res);
            routepoints = routepoints;
        })

        routepoints.splice(indexb, 1);

        routepoints = routepoints;
    }

    let leafletMap: LeafletMap;

</script>

<div class="main">
    <RouteOverview routes="{routepoints}" focus="{focus}" remove="{remove}" merge="{merge}" split="{split}"/>

    <LeafletMap bind:this={leafletMap} bind:options={mapOptions} on:click={onMapClick}>
        <TileLayer url={tileUrl} options={tileLayerOptions}/>
        <TileLayer url={railUrl} options={tileLayerOptions}/>

        {#each points as point}
            <CircleMarker latLng={[point.lat, point.lng]} radius="{15}"/>
        {/each}

        {#each routepoints as point}
            {#if point.type === RoutePointType.SingleStation}
                <CircleMarker latLng={[point.lat, point.lng]} color="{point.colour}" radius="{15}"/>
            {:else}
                {console.log(point.segments)}
                <Polyline latLngs={point.segments}>
                </Polyline>
                <CircleMarker latLng={[point.getLatFrom(), point.fromobj.getLngFrom()]} color="{point.colour}"
                              radius="{15}"/>
                <CircleMarker latLng={[point.getLatTo(), point.getLngTo()]} color="{point.colour}" radius="{15}"/>
            {/if}
        {/each}
    </LeafletMap>
</div>

<style>
    /* NOTE: Typically not imported from here, see documentation for more information. */
    @import 'https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.css';

    :global(html), :global(body) {
        margin: 0;
        padding: 0;
    }

    .main {
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: row;
    }
</style>
