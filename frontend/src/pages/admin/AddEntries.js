import React, { useState } from 'react';
import InnerComponent from './AddEntryForm';

const OuterComponent = ({ schema }) => {
    const [activeTable, setActiveTable] = useState(null);

    return (
        <div>
            {Object.entries(schema).map(([tableName, tableData]) => (
                <div key={tableName}>
                    <button onClick={() => setActiveTable(activeTable === tableName ? null : tableName)}>
                        {tableName}
                    </button>
                    {activeTable === tableName &&
                        <InnerComponent
                            tableName={tableName}
                            fields={tableData.fields}
                            url={tableData.url}
                        />}
                </div>
            ))}
        </div>
    );
};

export default OuterComponent;
