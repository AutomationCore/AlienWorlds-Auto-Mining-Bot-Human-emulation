waxjs = require("@waxio/waxjs/dist");
const { Serialize } = require("eosjs/dist/index.js");
const crypto = require("crypto-browserify/index.js");
fs = require('fs');

window.wax = new waxjs.WaxJS('https://api.waxsweden.org');

const getRand = () => {
            const arr = new Uint8Array(8);
            for (let i=0; i < 8; i++){
                const rand = Math.floor(Math.random() * 255);
                arr[i] = rand;
            }
            return arr;
        };

const pushRand = (sb) => {
    const arr = getRand();
    sb.pushArray(arr);
    return arr;
};

window.GenerateNonce = (mining_account, account, difficulty, last_mine_tx) => {
    let good = false, itr = 0, rand = 0, hash, sb, hex_digest, rand_arr;

    if (!last_mine_tx){
        console.error(`Please provide last mine tx`);
        return;
    }
    last_mine_tx = last_mine_tx.substr(0, 16); // only first 8 bytes of txid
    const last_mine_buf = Buffer.from(last_mine_tx, 'hex');
    const is_wam = account.substr(-4) === '.wam';
    // const is_wam = true;

    console.log(`Performing work with difficulty ${difficulty}, last tx is ${last_mine_tx}...`);
    if (is_wam){
        console.log(`Using WAM account`);
    }

    const start = (new Date()).getTime();

    while (!good){
        sb = new Serialize.SerialBuffer({
            textEncoder: new TextEncoder,
            textDecoder: new TextDecoder
        });
        sb.pushName(account);
        sb.pushArray(Array.from(last_mine_buf));
        rand_arr = pushRand(sb);
        hash = crypto.createHash("sha256");
        hash.update(sb.array.slice(0, 24));
        hex_digest = hash.digest('hex');
        // console.log(hex_digest);
        if (is_wam){
            // easier for .wam accounts
            good = hex_digest.substr(0, 4) === '0000';
        }
        else {
            // console.log(`non-wam account, mining is harder`)
            good = hex_digest.substr(0, 6) === '000000';
        }

        if (good){
            if (is_wam){
                last = parseInt(hex_digest.substr(4, 1), 16);
            }
            else {
                last = parseInt(hex_digest.substr(6, 1), 16);
            }
            good &= (last <= difficulty);
            // console.log(hex_digest);
        }
        itr++;

        if (itr % 50000000 === 0){
            console.log(`Still mining - tried ${itr} iterations`);
        }

        if (!good){
            // delete sb;
            // delete hash;
        }

    }
    const end = (new Date()).getTime();

    // console.log(sb.array.slice(0, 20));
    // const rand_str = Buffer.from(sb.array.slice(16, 24)).toString('hex');
    const rand_str = Array.from(rand_arr).map(i => ('0' + i.toString(16)).slice(-2)).join('');

    console.log(`Found hash in ${itr} iterations with ${account} ${rand_str}, last = ${last}, hex_digest ${hex_digest} taking ${(end-start) / 1000}s`)
    const mine_work = {account, rand_str, hex_digest};

    return mine_work;
};
//
//var args = process.argv.slice(2);
//return GenerateNonce(args[0], args[1], args[2], args[3]);
//
//fs.writeFile('mine_data/'+args[4]+'.txt', JSON.stringify(mine_work), function (err) {
//  if (err) return console.log(err);
//});