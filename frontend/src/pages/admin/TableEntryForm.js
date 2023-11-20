import React, { useState } from 'react';

const TableEntryForm = ({ tableName, fields, url }) => {
    const [formData, setFormData] = useState({});

    const handleChange = (e, field) => {
        setFormData({ ...formData, [field]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            const data = await response.json();
            if (response.ok) {
                console.log('Data saved successfully:', data);
            } else {
                console.error('Error saving data:', data);
            }
        } catch (error) {
            console.error('Network error:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            {fields.map(field => (
                <div key={field}>
                    <label>{field}:</label>
                    <input type="text" value={formData[field] || ''} onChange={e => handleChange(e, field)} />
                </div>
            ))}
            <button type="submit">Add Entry</button>
        </form>
    );
};

export default TableEntryForm;
