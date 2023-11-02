import React from "react";
import styles from "../css/ListResult.module.css";

function ListResult({ result }) {
    const imagePath = process.env.PUBLIC_URL + '/' + result.result_image;
    const leftLines = result.leftLines;
    const rightLines = result.rightLines;
    // Add any other store-specific details you want to display on the right side here.

    console.log(result);
    return (
        <div className={styles.listResult}>
            <img src={imagePath} alt={result.result_name} className={styles.resultImg} />
            <div className={styles.leftLines}>
                {leftLines.map((line, index) => <p key={index}>{line}</p>)}
            </div>
            <div className={styles.rightLines}>
                {rightLines.map((line, index) => <p key={index}>{line}</p>)}
            </div>
        </div>
    );
}

export default ListResult;
