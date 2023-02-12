/*
-------------STRING FORMATTING-------------
*/

function format(string, value) {
    let output = '';
    for (let i = 0; i < string.length; i++) {
        if (string[i] === '}' && string[i-1] === '{') {
            output += String(value);
        } else if (!(string[i] === '{' && string[i+1] === '}')) {
            output += string[i];
        }
    }
    return output;
}

function doubleFormat(string, value1, value2) {
    let output = '';
    for (let i = 0; i < string.length; i++) {
        if (string[i] === '}' && string[i - 1] === '{') {
            output += String(value1);
        } else if (string[i] === ']' && string[i - 1] === '[') {
            output += String(value2);
        } else if (!(string[i] === '{' && string[i+1] === '}' || string[i] === '[' && string[i+1] === ']')) {
            output += string[i];
        }
    }
    return output;
}



/*
-------------ADDING SYMBOLS AND INDICATORS-------------
 */

const indicatorElement = `<div class="panel panel-default">
                                <h5>Indicator {}</h5>
                                <div id="symbolsDiv{}">
                                    <div class="panel panel-default">
                                        <h5>Symbol {}.1</h5>
                                        <div class="form-group">
                                            <label for="sigType_{}_1">Type: </label>
                                            <select id="sigType_{}_1" name="sigType_{}_1">
                                                <option value="positive">positive</option>
                                                <option value="negative">negative</option>
                                            </select>
                                        </div>
                                        <div class="form-group">
                                            <label for="symbols_{}_1">Symbol: </label>
                                            <input id="symbols_{}_1" name="symbols_{}_1" type="text" class="form-inline" placeholder="Enter symbol">
                                        </div>
                                        <div class="form-group">
                                            <label for="multiplier_{}_1">Multiplier: </label>
                                            <input id="multiplier_{}_1" name="multiplier_{}_1" type="text" class="form-inline" placeholder="Enter multiplier">
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="addSymbol{}">Add Symbol</label>
                                    <button id="addSymbol{}" type="button" class="btn btn-default" onclick="addSymbol(1)">+</button>
                                </div>
                                <div class="form-group">
                                    <label for="aggregation{}">Aggregation: </label>
                                    <select id="aggregation{}" name="aggregation{}">
                                        <option value="sum">sum</option>
                                        <option value="average">average</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="priceType{}">Price Type: </label>
                                    <select id="priceType{}" name="priceType{}">
                                        <option value="percent">percent</option>
                                        <option value="absolute">absolute</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="thresholdType{}">Threshold type: </label>
                                    <select id="thresholdType{}" name="thresholdType{}">
                                        <option value="zscore">z-score</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="threshold{}">Threshold:</label>
                                    <input id="threshold{}" name="threshold{}" type="number" placeholder="Enter threshold" class="form-inline">
                                </div>
                                <div class="form-group">
                                    <label for="triggerType{}">Trigger Type:</label>
                                    <select id="triggerType{}" name="triggerType{}">
                                        <option value="filter">filter</option>
                                        <option value="break">break</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="triggerBias{}">Trigger Bias:</label>
                                    <select id="triggerBias{}" name="triggerBias{}">
                                        <option value="above">above</option>
                                        <option value="below">below</option>
                                    </select>
                                </div>
                            </div>`;
const symbolElement = `<div class="panel panel-default">
                                        <h5>Symbol {}.[]</h5>
                                        <div class="form-group">
                                            <label for="sigType_{}_[]">Type: </label>
                                            <select id="sigType_{}_[]" name="sigType_{}_[]">
                                                <option value="positive">positive</option>
                                                <option value="negative">negative</option>
                                            </select>
                                        </div>
                                        <div class="form-group">
                                            <label for="symbols_{}_[]">Symbol: </label>
                                            <input id="symbols_{}_[]" name="symbols_{}_[]" type="text" class="form-inline" placeholder="Enter symbol">
                                        </div>
                                        <div class="form-group">
                                            <label for="multiplier_{}_[]">Multiplier: </label>
                                            <input id="multiplier_{}_[]" name="multiplier_{}_[]" type="text" class="form-inline" placeholder="Enter multiplier">
                                        </div>
                                    </div>`;
let numIndicators = 1;
let numSymbols = [1];
let indicatorsButton = document.getElementById("addIndicator");
let symbolsButton = [document.getElementById("addSymbol1")];
let indicatorsDiv = document.getElementById("indicatorsDiv");
let symbolsDiv = [document.getElementById("symbolsDiv1")];

indicatorsButton.addEventListener('click', addIndicator);

function addIndicator() {
    numIndicators++;
    numSymbols.push(1);
    indicatorsDiv.insertAdjacentHTML('beforeend', format(indicatorElement, numIndicators));
    symbolsDiv.push(document.getElementById(format("symbolsDiv{}", numIndicators)));
    symbolsButton.push(document.getElementById(format("addSymbol{}", numIndicators)));
}


function addSymbol(indicatorNum) {
    numSymbols[indicatorNum - 1]++;
    symbolsDiv[indicatorNum - 1].insertAdjacentHTML('beforeend', doubleFormat(symbolElement, indicatorNum, numSymbols[indicatorNum - 1]));
}


/*
-------------ADDING TRADE STRUCTURES FUNCTIONALITY-------------
*/
let numTradeStructures = 1;
let tradeStructureButton = document.getElementById("addTradeStructure");
let tradeStructureDiv = document.getElementById("tradeStructureDiv");
const tradeStructureElement = `<div class="panel panel-default">
                                <h5>Trade Structure {}</h5>
                                <div class="form-group">
                                    <label for="type{}">Type: </label>
                                    <select id="type{}" name="type{}">
                                        <option value="long">long</option>
                                        <option value="short">short</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="ticker{}">Ticker: </label>
                                    <input id="ticker{}" name="ticker{}" type="text" class="form-inline" placeholder="Enter ticker">
                                </div>
                                <div class="form-group">
                                    <label for="execution{}">Execution: </label>
                                    <select id="execution{}" name="execution{}">
                                        <option value="market">market</option>
                                        <option value="limit">limit</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="order{}">Order: </label>
                                    <input id="order{}" name="order{}" type="text" class="form-inline" placeholder="Enter order">
                                </div>
                                <div class="form-group">
                                    <label for="takeProfit{}">Take Profit: </label>
                                    <input id="takeProfit{}" name="takeProfit{}" type="number" class="form-inline" placeholder="Enter take profit">
                                </div>
                                <div class="form-group">
                                    <label for="stopLoss{}">Stop Loss: </label>
                                    <input id="stopLoss{}" name="stopLoss{}" type="number" class="form-inline" placeholder="Enter stop loss" step="any">
                                </div>
                                <div class="form-group">
                                    <label for="marketOnClose{}">Market On Close: </label>
                                    <input id="marketOnClose{}" name="marketOnClose{}" type="number" class="form-inline" placeholder="Enter market on close" step="1">
                                </div>
                            </div>`;
tradeStructureButton.addEventListener("click", addTradeStructure);

function addTradeStructure() {
    numTradeStructures++;
    tradeStructureDiv.insertAdjacentHTML('beforeend', format(tradeStructureElement, numTradeStructures));
}
