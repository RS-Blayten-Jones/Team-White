
<template>
  <div class="data-table">
    <div v-if="!rows.length" class="empty-state">
      No results found.
    </div>

    <table v-else class="table">
      <thead>
        <tr>
          <th v-for="col in visibleColumns" :key="col">
            {{ headerMap[col] ?? startCase(col) }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rIdx) in rows" :key="rowKey(row, rIdx)">
          <td v-for="col in visibleColumns" :key="col">
            <slot name="cell" :row="row" :column="col" :value="row[col]">
              {{ formatValue(row[col]) }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="count">
      Showing {{ rows.length }} item{{ rows.length === 1 ? '' : 's' }}.
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'

type Row = Record<string, any>

export default defineComponent({
  name: 'DataTable',
  props: {
    data: {
      type: Array as () => Row[],
      required: true
    },
    /**
     * Optional explicit column order. If provided, table will use these first,
     * then append any remaining discovered columns not listed here.
     */
    columns: {
      type: Array as () => string[],
      required: false,
      default: () => []
    },
    /**
     * Optional map of column keys to human-friendly headers.
     * e.g., { id: 'ID', text: 'Text', status: 'Status' }
     */
    headerMap: {
      type: Object as () => Record<string, string>,
      required: false,
      default: () => ({})
    },
    /**
     * Optional set of columns to hide (by key).
     */
    hiddenColumns: {
      type: Array as () => string[],
      required: false,
      default: () => []
    },
    /**
     * Optional function to derive a stable unique key for a row.
     */
    getRowKey: {
      type: Function as unknown as () => ((row: Row, index: number) => string | number),
      required: false,
      default: (row: Row, index: number) => row.id ?? index
    }
  },
  setup(props) {
    const discoveredColumns = computed(() => {
      const set = new Set<string>()
      for (const row of props.data) {
        Object.keys(row ?? {}).forEach(k => set.add(k))
      }
      return Array.from(set)
    })

    const mergedColumns = computed(() => {
      if (!props.columns.length) return discoveredColumns.value
      // Keep specified order, then add any others discovered
      const specified = props.columns
      const extras = discoveredColumns.value.filter(c => !specified.includes(c))
      return [...specified, ...extras]
    })

    const visibleColumns = computed(() =>
      mergedColumns.value.filter(c => !props.hiddenColumns.includes(c))
    )

    const rowKey = (row: Row, index: number) => props.getRowKey(row, index)

    const startCase = (key: string) =>
      key
        .replace(/[_\-]+/g, ' ')
        .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
        .replace(/\s+/g, ' ')
        .replace(/^./, s => s.toUpperCase())

    const formatValue = (val: any) => {
      if (val === null || val === undefined) return ''
      if (typeof val === 'boolean') return val ? 'Yes' : 'No'
      if (Array.isArray(val)) return val.map(v => (typeof v === 'object' ? JSON.stringify(v) : String(v))).join(', ')
      if (typeof val === 'object') return JSON.stringify(val)
      return String(val)
    }

    return {
      visibleColumns,
      headerMap: props.headerMap,
      rowKey,
      startCase,
      formatValue,
      rows: props.data
    }
  }
})
</script>

<style scoped>
.data-table {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background-color: var(--bg-tertiary);
  padding: var(--spacing-md);
}

.table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  text-align: left;
  padding: 0.75rem;
  border-bottom: 2px solid var(--border-color);
  color: var(--text-primary);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  background: var(--bg-secondary);
}

tbody td {
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

tbody tr:hover td {
  background: rgba(0, 0, 0, 0.03);
}

.empty-state {
  color: var(--text-secondary);
  font-style: italic;
}

.count {
  margin-top: var(--spacing-sm);
  color: var(--text-secondary);
  font-size: var(--font-size-xs);
}
</style>
