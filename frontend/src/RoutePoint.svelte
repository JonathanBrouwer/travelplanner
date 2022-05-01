<script lang="ts">
    import {RoutePoint, RoutePointType} from "./data";
    import Fa from 'svelte-fa/src/fa.svelte'
    import {faCircleXmark, faRightFromBracket, faRightToBracket, faScissors} from '@fortawesome/free-solid-svg-icons'

    export let route: RoutePoint;
    export let remove: () => void;
    export let split: () => void;
</script>
{#if route.type === RoutePointType.SingleStation}
    <div class="rp single">
        <div class="colour-wrapper">
            <div class="colour" style="background-color: {route.colour}"></div>
        </div>
        <div class="description">{route.description}</div>
        <div class="remove-wrapper">
            <div class="remove" on:click|stopPropagation={remove}>
                <Fa icon="{faCircleXmark}"/>
            </div>
        </div>
    </div>
{:else}
    <div class="rp route">
        <div class="colour-wrapper">
            <div class="colour" style="background-color: {route.colour}"></div>
        </div>

        <div class="from">
            <Fa icon="{faRightFromBracket}"/>
            {route.from}
        </div>
        <div class="to">
            <Fa icon="{faRightToBracket}"/>
            {route.to}
        </div>
        <div class="remove-wrapper">
            <div class="remove" on:click|stopPropagation={remove}>
                <Fa icon="{faCircleXmark}"/>
            </div>
        </div>

        <div class="split-wrapper">
            <div class="split" on:click|stopPropagation={split}>
                <Fa icon="{faScissors}"/>
            </div>
        </div>
    </div>
{/if}

<style>
    .remove:hover {
        background-color: orangered;
    }

    .split:hover {
        background-color: orangered;
    }

    .remove {
        height: 1.5em;
        width: 1.5em;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .remove-wrapper {
        grid-area: remove;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .split {
        height: 1.5em;
        width: 1.5em;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .split-wrapper {
        grid-area: split;
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


    .from {
        grid-area: from;
        display: flex;
        flex-direction: row;
        align-items: center;

        gap: 1em;
    }

    .to {
        grid-area: to;
        display: flex;
        flex-direction: row;
        align-items: center;

        gap: 1em;
    }

    .rp {
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 3em auto 2em;
        grid-template-rows: auto;
        background-color: transparent;
    }

    .single {
        grid-template-areas:
            "colour description remove"
            "colour subtext other";
    }
    .route {
        grid-template-areas:
            "colour from remove"
            "colour to split"
    }
</style>
