import React, { useState } from 'react';
import TableEntryForm from './TableEntryForm';

const AddEntries = ({ schema }) => {
    const [activeTable, setActiveTable] = useState('');

    const handleDropdownChange = (event) => {
        setActiveTable(event.target.value);
    };

    return (
        <div>
            <h2>Add Entries</h2>
            <select value={activeTable} onChange={handleDropdownChange}>
                <option value="">Select a table</option>
                {Object.keys(schema).map(tableName => (
                    <option key={tableName} value={tableName}>
                        {tableName}
                    </option>
                ))}
            </select>

            {activeTable && (
                <TableEntryForm
                    tableName={activeTable}
                    fields={schema[activeTable].fields}
                    url={schema[activeTable].url}
                />
            )}
        </div>
    );
};

export default AddEntries;
