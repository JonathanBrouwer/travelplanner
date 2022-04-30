<script lang="ts">
    import {RoutePoint} from "./data";
    import Fa from 'svelte-fa/src/fa.svelte'
    import { faCross } from '@fortawesome/free-solid-svg-icons'

    export let route: RoutePoint;
</script>

<div class="rp">
    <div class="colour-wrapper">
        <div class="colour" style="background-color: {route.colour}"></div>
    </div>
    <div class="description">{route.description}</div>
    <div class="remove-wrapper">
        <div class="remove">
            <Fa icon="{faCross}" />
        </div>
    </div>
</div>

<style>
    .remove {
        height: 1em;
        width: 1em;
        border-radius: 50%;
        display: inline-block;
    }

    .remove-wrapper {
        grid-area: remove;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .colour-wrapper {
        grid-area: colour;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .colour {
        height: 2em;
        width: 2em;
        border-radius: 50%;
        display: inline-block;
    }

    .description {
        grid-area: description;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .rp {
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 5em auto 1em;
        grid-template-rows: auto;
        grid-template-areas:
            "colour description remove"
            "colour subtext other";
        background-color: transparent;
    }
</style>
