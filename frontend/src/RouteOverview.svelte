<script lang="ts">
    import Route from "./RoutePoint.svelte";
    import {RoutePoint, RoutePointType} from "./data";
    import {flip} from 'svelte/animate';

    let routes = [
        RoutePoint.randomColour("Amsterdam", RoutePointType.SingleStation),
        RoutePoint.randomColour("Delft", RoutePointType.SingleStation),
        RoutePoint.randomColour("Maastricht", RoutePointType.SingleStation),
        RoutePoint.randomColour("Rotterdam", RoutePointType.SingleStation),
    ];

    let selected = null;
    let hovering = null;

    const drop = (event, target) => {
        event.dataTransfer.dropEffect = 'move';
        const start = parseInt(event.dataTransfer.getData("text/plain"));
        const newTracklist = routes

        if (start < target) {
            newTracklist.splice(target + 1, 0, newTracklist[start]);
            newTracklist.splice(start, 1);
        } else {
            newTracklist.splice(target, 0, newTracklist[start]);
            newTracklist.splice(start + 1, 1);
        }
        routes = newTracklist;
        hovering = null;
    }

    const dragstart = (event, i) => {
        event.dataTransfer.effectAllowed = 'move';
        event.dataTransfer.dropEffect = 'move';
        event.dataTransfer.setData('text/plain', i);
    }

    const dragenter = (index) => {
        hovering = index;
        selected = index;
    }

</script>

<div class="route-overview">
    <input type="text">
    {#each routes as route, index (index)}
        <div
                class="list-item"
                animate:flip
                draggable=true
                on:dragstart={event => dragstart(event, index)}
                on:drop|preventDefault={event => drop(event, index)}
                ondragover="return false"
                on:dragenter={() => dragenter(index)}
                on:click={() => selected=index}
                class:is-active={selected === index}>
            <Route route="{route}"/>
        </div>
    {/each}
</div>

<style>
    .route-overview {
        height: 100%;
        background-color: white;
        border-radius: 4px;
        box-shadow: 0 2px 3px rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.1);
        width: 30em;
    }

    .list-item {
        display: block;
        padding: 0.5em 1em;
        width: 100%;
        height: 5em;
        cursor: pointer;
    }

    .list-item:not(:last-child) {
        border-bottom: 1px solid #dbdbdb;
    }

    .list-item.is-active {
        background-color: #3273dc;
        color: #fff;
    }
</style>