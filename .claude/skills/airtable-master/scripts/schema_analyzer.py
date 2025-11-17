#!/usr/bin/env python3
"""
Schema Analyzer for Airtable

Generates comprehensive schema documentation including:
- Entity-relationship diagrams (ASCII art)
- Field statistics and usage patterns
- Relationship mapping
- View configuration summaries
- Schema complexity metrics

Usage:
    from scripts.schema_analyzer import SchemaAnalyzer

    analyzer = SchemaAnalyzer(base_schema)
    docs = analyzer.generate_documentation()
"""

from typing import Dict, Any, List
from collections import Counter


class SchemaAnalyzer:
    """Analyze and document Airtable base schemas"""

    def __init__(self, base_schema: Dict[str, Any]):
        """
        Initialize analyzer with base schema

        Args:
            base_schema: Complete base schema from getBaseSchema
        """
        self.schema = base_schema
        self.tables = base_schema.get("tables", [])
        self.relationships = self._extract_relationships()

    def generate_documentation(self, output_format: str = "markdown") -> str:
        """
        Generate complete schema documentation

        Args:
            output_format: 'markdown' or 'text'

        Returns:
            Formatted documentation string
        """
        doc = []

        # Header
        doc.append(self._generate_header())

        # Overview statistics
        doc.append(self._generate_overview())

        # Relationship diagram
        doc.append(self._generate_relationship_diagram())

        # Table details
        doc.append(self._generate_table_details())

        # Field statistics
        doc.append(self._generate_field_statistics())

        # Complexity metrics
        doc.append(self._generate_complexity_metrics())

        return "\n\n".join(doc)

    def _generate_header(self) -> str:
        """Generate documentation header"""
        return f"""# Airtable Base Schema Documentation

**Generated:** {self._get_timestamp()}
**Tables:** {len(self.tables)}
**Total Fields:** {sum(len(t.get("fields", [])) for t in self.tables)}
"""

    def _generate_overview(self) -> str:
        """Generate overview statistics"""
        total_fields = sum(len(t.get("fields", [])) for t in self.tables)
        total_views = sum(len(t.get("views", [])) for t in self.tables)

        field_types = Counter()
        for table in self.tables:
            for field in table.get("fields", []):
                field_types[field.get("type", "unknown")] += 1

        overview = [
            "## Overview",
            "",
            f"**Total Tables:** {len(self.tables)}",
            f"**Total Fields:** {total_fields}",
            f"**Total Views:** {total_views}",
            f"**Total Relationships:** {len(self.relationships)}",
            "",
            "### Field Type Distribution",
            "",
        ]

        for field_type, count in field_types.most_common():
            overview.append(f"- `{field_type}`: {count}")

        return "\n".join(overview)

    def _generate_relationship_diagram(self) -> str:
        """Generate ASCII relationship diagram"""
        diagram = ["## Entity Relationship Diagram", "", "```"]

        # Simple ASCII representation
        for table in self.tables:
            table_name = table.get("name", "Unknown")
            diagram.append(f"┌─ {table_name}")

            # Show linked fields
            for field in table.get("fields", []):
                if field.get("type") == "multipleRecordLinks":
                    options = field.get("options", {})
                    linked_table_id = options.get("linkedTableId")
                    if linked_table_id:
                        linked_table = self._get_table_by_id(linked_table_id)
                        if linked_table:
                            field_name = field.get("name", "Unknown")
                            linked_name = linked_table.get("name", "Unknown")
                            diagram.append(f"│  └─> {field_name} → {linked_name}")

            diagram.append("│")

        diagram.append("```")
        return "\n".join(diagram)

    def _generate_table_details(self) -> str:
        """Generate detailed table documentation"""
        details = ["## Table Details", ""]

        for table in self.tables:
            table_name = table.get("name", "Unknown")
            table_id = table.get("id", "Unknown")
            description = table.get("description", "No description")

            details.append(f"### {table_name}")
            details.append("")
            details.append(f"**ID:** `{table_id}`")
            details.append(f"**Description:** {description}")
            details.append(f"**Fields:** {len(table.get('fields', []))}")
            details.append(f"**Views:** {len(table.get('views', []))}")
            details.append("")

            # Fields table
            details.append("#### Fields")
            details.append("")
            details.append("| Name | Type | Description |")
            details.append("|------|------|-------------|")

            for field in table.get("fields", []):
                name = field.get("name", "Unknown")
                field_type = field.get("type", "unknown")
                desc = field.get("description", "-")

                # Handle linked fields
                if field_type == "multipleRecordLinks":
                    options = field.get("options", {})
                    linked_table_id = options.get("linkedTableId")
                    linked_table = self._get_table_by_id(linked_table_id)
                    if linked_table:
                        field_type = f"{field_type} → {linked_table.get('name')}"

                details.append(f"| {name} | `{field_type}` | {desc} |")

            details.append("")

            # Views
            if table.get("views"):
                details.append("#### Views")
                details.append("")
                for view in table.get("views", []):
                    view_name = view.get("name", "Unknown")
                    view_type = view.get("type", "unknown")
                    details.append(f"- **{view_name}** (`{view_type}`)")
                details.append("")

        return "\n".join(details)

    def _generate_field_statistics(self) -> str:
        """Generate field usage statistics"""
        stats = ["## Field Statistics", ""]

        # Collect statistics
        field_types = Counter()
        field_with_descriptions = 0
        total_fields = 0
        fields_with_options = 0

        for table in self.tables:
            for field in table.get("fields", []):
                total_fields += 1
                field_type = field.get("type", "unknown")
                field_types[field_type] += 1

                if field.get("description"):
                    field_with_descriptions += 1

                if field.get("options"):
                    fields_with_options += 1

        desc_pct = (
            (field_with_descriptions / total_fields * 100) if total_fields > 0 else 0
        )
        opts_pct = (fields_with_options / total_fields * 100) if total_fields > 0 else 0

        stats.append(f"**Total Fields:** {total_fields}")
        stats.append(
            f"**Fields with Descriptions:** {field_with_descriptions} ({desc_pct:.1f}%)"
        )
        stats.append(
            f"**Fields with Options:** {fields_with_options} ({opts_pct:.1f}%)"
        )
        stats.append("")

        stats.append("### Most Common Field Types")
        stats.append("")
        for field_type, count in field_types.most_common(10):
            pct = (count / total_fields * 100) if total_fields > 0 else 0
            stats.append(f"- `{field_type}`: {count} ({pct:.1f}%)")

        return "\n".join(stats)

    def _generate_complexity_metrics(self) -> str:
        """Generate schema complexity metrics"""
        metrics = ["## Complexity Metrics", ""]

        # Calculate metrics
        avg_fields = (
            sum(len(t.get("fields", [])) for t in self.tables) / len(self.tables)
            if self.tables
            else 0
        )
        avg_views = (
            sum(len(t.get("views", [])) for t in self.tables) / len(self.tables)
            if self.tables
            else 0
        )

        # Most complex table
        most_complex = max(
            self.tables, key=lambda t: len(t.get("fields", [])), default=None
        )

        # Relationship density
        total_possible_relationships = len(self.tables) * (len(self.tables) - 1)
        relationship_density = (
            (len(self.relationships) / total_possible_relationships * 100)
            if total_possible_relationships > 0
            else 0
        )

        metrics.append(f"**Average Fields per Table:** {avg_fields:.1f}")
        metrics.append(f"**Average Views per Table:** {avg_views:.1f}")
        metrics.append(f"**Total Relationships:** {len(self.relationships)}")
        metrics.append(f"**Relationship Density:** {relationship_density:.1f}%")
        metrics.append("")

        if most_complex:
            metrics.append(
                f"**Most Complex Table:** {most_complex.get('name')} ({len(most_complex.get('fields', []))} fields)"
            )

        # Complexity score (arbitrary scale)
        complexity_score = (
            len(self.tables) * 1.0
            + avg_fields * 0.5
            + len(self.relationships) * 2.0
            + avg_views * 0.3
        )

        metrics.append("")
        metrics.append(f"**Complexity Score:** {complexity_score:.1f}")

        if complexity_score < 50:
            assessment = "Simple - Easy to understand and maintain"
        elif complexity_score < 150:
            assessment = "Moderate - Manageable with good documentation"
        elif complexity_score < 300:
            assessment = "Complex - Requires careful management"
        else:
            assessment = "Very Complex - Consider simplification"

        metrics.append(f"**Assessment:** {assessment}")

        return "\n".join(metrics)

    def _extract_relationships(self) -> List[Dict[str, Any]]:
        """Extract all relationships from schema"""
        relationships = []

        for table in self.tables:
            for field in table.get("fields", []):
                if field.get("type") == "multipleRecordLinks":
                    options = field.get("options", {})
                    linked_table_id = options.get("linkedTableId")

                    if linked_table_id:
                        relationships.append(
                            {
                                "from_table": table.get("name"),
                                "from_table_id": table.get("id"),
                                "field": field.get("name"),
                                "field_id": field.get("id"),
                                "to_table_id": linked_table_id,
                                "to_table": self._get_table_by_id(linked_table_id).get(
                                    "name"
                                )
                                if self._get_table_by_id(linked_table_id)
                                else "Unknown",
                            }
                        )

        return relationships

    def _get_table_by_id(self, table_id: str) -> Dict[str, Any]:
        """Get table by ID"""
        for table in self.tables:
            if table.get("id") == table_id:
                return table
        return {}

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Example usage
if __name__ == "__main__":
    # Example schema
    example_schema = {
        "tables": [
            {
                "id": "tbl1",
                "name": "Customers",
                "description": "Customer database",
                "fields": [
                    {"id": "fld1", "name": "Name", "type": "singleLineText"},
                    {"id": "fld2", "name": "Email", "type": "email"},
                    {
                        "id": "fld3",
                        "name": "Orders",
                        "type": "multipleRecordLinks",
                        "options": {"linkedTableId": "tbl2"},
                    },
                ],
                "views": [{"id": "viw1", "name": "All Customers", "type": "grid"}],
            },
            {
                "id": "tbl2",
                "name": "Orders",
                "description": "Order tracking",
                "fields": [
                    {"id": "fld4", "name": "Order Number", "type": "autonumber"},
                    {"id": "fld5", "name": "Amount", "type": "currency"},
                    {
                        "id": "fld6",
                        "name": "Customer",
                        "type": "multipleRecordLinks",
                        "options": {"linkedTableId": "tbl1"},
                    },
                ],
                "views": [{"id": "viw2", "name": "All Orders", "type": "grid"}],
            },
        ]
    }

    analyzer = SchemaAnalyzer(example_schema)
    documentation = analyzer.generate_documentation()

    print(documentation)

    # Save to file
    with open("schema_documentation.md", "w") as f:
        f.write(documentation)
    print("\n✓ Documentation saved to schema_documentation.md")
