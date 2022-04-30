<script lang="ts">
    import Route from "./RoutePoint.svelte";
    import {flip} from 'svelte/animate';
    import Fa from "svelte-fa";
    import {faLink} from "@fortawesome/free-solid-svg-icons";

    export let routes;
    export let focus;
    export let remove;
    export let merge;

    let selected = null;
    let hovering = null;

    let inputValue = "";

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

    const select = (index) => {
        selected = index;

        focus(routes[index].lat, routes[index].lng);
    }

    const handleInput = () => {

    }
</script>

<div class="route-overview">
    <input type="text" on:input={handleInput} bind:value={inputValue}>
    {#each routes as route, index (index)}
        <div
                class="list-item"
                animate:flip
                draggable=true
                on:dragstart={event => dragstart(event, index)}
                on:drop|preventDefault={event => drop(event, index)}
                ondragover="return false"
                on:dragenter={() => dragenter(index)}
                on:click={() => select(index)}
                class:is-active={selected === index}>
            <Route route="{route}" remove="{() => remove(index)}"/>

            {#if index !== routes.length - 1}
                <div class="link" on:click={merge(index, index + 1)}>
                    <Fa icon="{faLink}" />
                </div>
            {/if}
        </div>
    {/each}
</div>

<style>
    .link:hover {
        background-color: #99999999;
    }
    .link {
        position: relative;
        left: calc(50% - 1em);
        bottom: 0.3em;
        width: fit-content;
        border-radius: 50%;
        padding: 0.3em;
        color: #333333;
    }

    .route-overview {
        height: 100%;
        background-color: white;
        border-radius: 4px;
        box-shadow: 0 2px 3px rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.1);
        width: 30em;
        overflow-y: scroll;
    }

    .list-item {
        display: block;
        padding: 0.5em 1em;
        box-sizing: border-box;
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