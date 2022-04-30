<script lang="ts">
    import {CircleMarker, LeafletMap, TileLayer} from 'svelte-leafletjs';
    import {onMount} from "svelte";
    import {LatLng, LeafletMouseEvent} from "leaflet";
    import RouteOverview from "./RouteOverview.svelte";
    import {getClosestStation, Point} from "./api";
    import {RoutePoint, RoutePointType} from "./data";

    let routepoints: RoutePoint[] = [
        // RoutePoint.randomColour("Amsterdam", RoutePointType.SingleStation, 0, 0),
        // RoutePoint.randomColour("Delft", RoutePointType.SingleStation, 0, 0),
        // RoutePoint.randomColour("Maastricht", RoutePointType.SingleStation, 0, 0),
        // RoutePoint.randomColour("Rotterdam", RoutePointType.SingleStation, 0, 0),
    ];
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
            routepoints = [...routepoints, RoutePoint.randomColour(
                closest.name,
                RoutePointType.SingleStation,
                closest.lat,
                closest.lng,
            )];
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

    let leafletMap: LeafletMap;
</script>

<div class="main">
    <RouteOverview routes="{routepoints}"/>

    <LeafletMap bind:this={leafletMap} bind:options={mapOptions} on:click={onMapClick}>
        <TileLayer url={tileUrl} options={tileLayerOptions}/>
        <TileLayer url={railUrl} options={tileLayerOptions}/>

        {#each points as point}
            <CircleMarker latLng={[point.lat, point.lng]} />
        {/each}

        {#each routepoints as point}
            <CircleMarker latLng={[point.lat, point.lng]} color="{point.colour}"/>
        {/each}
        <!--        <Polygon latLngs={TestData.sentosaPolygon} color="#ff0000" fillColor="#ff0000">-->
        <!--            <Popup>Sentosa</Popup>-->
        <!--            <Tooltip>Sentosa</Tooltip>-->
        <!--        </Polygon>-->
        <!--{#each TestData.sentosaPolygon as point}-->
        <!--    <CircleMarker latLng={point} radius={3} color="#ff0000" fillColor="#ff0000">-->
        <!--        <Popup>{point}</Popup>-->
        <!--        <Tooltip>{point}</Tooltip>-->
        <!--    </CircleMarker>-->
        <!--{/each}-->
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
